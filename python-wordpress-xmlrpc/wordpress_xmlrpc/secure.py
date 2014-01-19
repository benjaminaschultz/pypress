from wordpress_xmlrpc.compat import xmlrpc_client
import base64 as b64
import hashlib as hl
import binascii as ba
try:
    import gzip
except ImportError:
    gzip = None #python can be built without zlib/gzip support


##
# Transport class for XML-RPC over HTTP, with public/private key authentication
# <p>
# You can override to create custom transports by subclassing this class and
# overriding selected methods
class SecureTransport(xmlrpc_client.Transport):
  def __init__(self, public_key, private_key, use_datetime=0):
    xmlrpc_client.Transport.__init__(self,use_datetime) 
    self.public_key = public_key
    self.private_key = private_key
  #compute authorization header and insert into request
  def send_request(self, connection, handler, request_body):
      #pk_hash = b64.b64encode(hl.sha256(self.private_key+request_body).hexdigest())
      pk_hash = hl.sha256(self.private_key+request_body).hexdigest()
      auth_header = self.public_key+'||'+pk_hash
      if (self.accept_gzip_encoding and gzip):
          connection.putrequest("POST", handler, skip_accept_encoding=True)
          connection.putheader("Accept-Encoding", "gzip")
          connection.putheader("Authorization",auth_header)
      else:
          connection.putrequest("POST", handler)
          connection.putheader("Authorization",auth_header)

##
# Transport class for XML-RPC over HTTP, with public/private key authentication
# <p>
class SecureSafeTransport(SecureTransport):

  def make_connection(self, host):
      if self._connection and host == self._connection[0]:
          return self._connection[1]
      # create a HTTPS connection object from a host descriptor
      # host may be a string, or a (host, x509-dict) tuple
      try:
          HTTPS = httplib.HTTPSConnection
      except AttributeError:
          raise NotImplementedError(
              "your version of httplib doesn't support HTTPS"
              )
      else:
          chost, self._extra_headers, x509 = self.get_host_info(host)
          self._connection = host, HTTPS(chost, None, **(x509 or {}))
          return self._connection[1]

  
class SecureServerProxy(xmlrpc_client.ServerProxy):
  def __init__(self, uri, transport=None, encoding=None, verbose=0,
               allow_none=0, use_datetime=0,public_key=None,private_key=None):

    if transport is None:
        if type == "https":
            transport = SecureSafeTransport(use_datetime=use_datetime,public_key=public_key,private_key=private_key)
        else:
            transport = SecureTransport(use_datetime=use_datetime,public_key=public_key,private_key=private_key)
    xmlrpc_client.ServerProxy.__init__(self, uri, transport, encoding, verbose,
               allow_none, use_datetime)

