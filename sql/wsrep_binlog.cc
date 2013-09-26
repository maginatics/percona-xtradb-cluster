/* Copyright 2013 Codership Oy <http://www.codership.com>

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; version 2 of the License.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program; if not, write to the Free Software
   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA */

#include "wsrep_priv.h"

/*
  Write the contents of a cache to memory buffer.

  This function quite the same as MYSQL_BIN_LOG::write_cache(),
  with the exception that here we write in buffer instead of log file.
 */
int wsrep_write_cache(IO_CACHE *cache, uchar **buf, size_t *buf_len)
{
  *buf= NULL;
  *buf_len= 0;

  my_off_t saved_pos= my_b_tell(cache);

  if (reinit_io_cache(cache, READ_CACHE, 0, 0, 0))
  {
    WSREP_ERROR("failed to initialize io-cache");
    return ER_ERROR_ON_WRITE;
  }

  uint length= my_b_bytes_in_cache(cache);
  long long total_length= 0;

  do
  {
    total_length += length;
    /* bail out if buffer grows too large
       This is a temporary fix to avoid allocating indefinitely large buffer,
       not a real limit on a writeset size which includes other things like
       header and keys.
     */
    if (total_length > wsrep_max_ws_size)
    {
      WSREP_WARN("transaction size limit (%lld) exceeded: %lld",
                 wsrep_max_ws_size, total_length);
      goto error;
    }

#ifndef DBUG_OFF /* my_realloc() asserts on zero length */
    if (total_length) {
#endif
    uchar* tmp= (uchar *)my_realloc(*buf, total_length, MYF(0));
    if (!tmp)
    {
      WSREP_ERROR("could not (re)allocate buffer: %zu + %u", *buf_len, length);
      goto error;
    }
    *buf= tmp;
#ifndef DBUG_OFF
    }
#endif

    memcpy(*buf + *buf_len, cache->read_pos, length);
    *buf_len= total_length;
    cache->read_pos= cache->read_end;
  } while ((cache->file >= 0) && (length= my_b_fill(cache)));

  if (reinit_io_cache(cache, WRITE_CACHE, saved_pos, 0, 0))
  {
    WSREP_ERROR("failed to initialize io-cache");
    goto cleanup;
  }

  return 0;

error:
  if (reinit_io_cache(cache, WRITE_CACHE, saved_pos, 0, 0))
  {
    WSREP_WARN("failed to initialize io-cache");
  }
cleanup:
  my_free(*buf);
  *buf= NULL;
  *buf_len= 0;
  return ER_ERROR_ON_WRITE;
}

extern handlerton *binlog_hton;

/*
  wsrep exploits binlog's caches even if binlogging itself is not
  activated. In such case connection close needs calling
  actual binlog's method.
  Todo: split binlog hton from its caches to use ones by wsrep
  without referring to binlog's stuff.
*/
int wsrep_binlog_close_connection(THD* thd)
{
  DBUG_ENTER("wsrep_binlog_close_connection");
  if (thd_get_ha_data(thd, binlog_hton) != NULL)
    binlog_hton->close_connection (binlog_hton, thd);
  DBUG_RETURN(0);
}

int wsrep_binlog_savepoint_set(THD *thd,  void *sv)
{
  if (!wsrep_emulate_bin_log) return 0;
  int rcode = binlog_hton->savepoint_set(binlog_hton, thd, sv);
  return rcode;
}
int wsrep_binlog_savepoint_rollback(THD *thd, void *sv)
{
  if (!wsrep_emulate_bin_log) return 0;
  int rcode = binlog_hton->savepoint_rollback(binlog_hton, thd, sv);
  return rcode;
}
