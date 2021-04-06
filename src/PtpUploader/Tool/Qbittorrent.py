from ..MyGlobals import MyGlobals
from ..PtpUploaderException import PtpUploaderException
from ..Settings import Settings

import qbittorrentapi

class Qbittorrent:
	def __init__( self, host, port, username, password ):
		MyGlobals.Logger.info( "Initializing qbittorrent." )
		self.qbittorrent = qbittorrentapi.Client(host=host, port=port, username=username, password=password)

	# downloadPath is the final path. Suggested directory name from torrent won't be added to it.
	# Returns with the info hash of the torrent.
	def AddTorrent(self, logger=None, torrentPath=None, downloadPath=None):
		logger.info( "Initiating the download of torrent '%s' with qBittorrent to '%s'." % ( torrentPath, downloadPath ) );
		self.qbittorrent.torrents_add(torrent_files=torrentPath, save_path=downloadPath)
		# Not sure if returning hash works yet.
		return (subprocess.check_output(f'lstor {torrentPath} -o __hash__ -q', stderr=subprocess.STDOUT)).decode("utf-8")

	def AddTorrentSkipHashCheck(self, logger, torrentPath, downloadPath):
		logger.info( "Adding torrent '%s' without hash checking to qBittorrent to '%s'." % ( torrentPath, downloadPath ) );
		torrent = self.qbittorrent.torrents_add(torrent_files=torrentPath, save_path=downloadPath, is_skip_checking=True)
		return torrent.hashString

	def IsTorrentFinished(self, infoHash):
		try:
			for thing in self.qbittorrent.torrents_info():
				if thing.hash == infoHash:
					if thing.state_enum.is_complete:
						return True
		except Exception:
			logger.exception("Got exception while trying to check torrent's completion status. Info hash: '%s'." % infoHash);
		return False

	# It doesn't delete the data.
	def DeleteTorrent(self, logger, infoHash):
		try:
			self.torrents_delete(self, delete_files=False, torrent_hashes=infoHash)
		except Exception:
			logger.exception( "Got exception while trying to delete torrent. Info hash: '%s'." % infoHash )

	# qBittorrent doesn't have any problems with this.. so just skip
	def CleanTorrentFile(self, logger, torrentPath):
		# logger.info( "Cleaning torrent file '%s'... nah" % torrentPath )
		pass
