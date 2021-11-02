<?php
/*
TorrentLoad v1.3.1
23/02/14
Created by Matt Dyson
mattdyson.org

See mattdyson.org/projects/torrentload for more details

An alternative to using server.py - this PHP script will accept magnet details and write out a valid .torrent
file into a watch folder for rTorrent to pick up

Note that folder permissions may be an issue when using this - your watch folder will need to be writable from
whatever user this PHP script is running under, and the torrent files will need to be readable
*/

$magnetPath = "/home/matt/download/watch"; // Watch directory for torrents
$secret = trim(file_get_contents('secret'));

// Thanks to http://stackoverflow.com/questions/353379/how-to-get-multiple-parameters-with-same-name-from-a-url-in-php
$query  = explode('&', $_SERVER['QUERY_STRING']);
$params = array();

foreach($query as $param) {
    list($name, $value) = explode('=', $param);
    $params[urldecode($name)][] = urldecode($value);
}

if(!$_GET[xt]) { die("Did not recognise a valid torrent link"); }
if($_GET[secret]!=$secret) { die("Secret key invalid"); }

$link = "magnet:?xt=".$_GET["xt"]."&dn=".urlencode($_GET["dn"]);

foreach($params["tr"] as $key=>$val) {
	$link.="&tr=".urlencode($val);
}

$content = "d10:magnet-uri".strlen($link).":".$link."e";

$e = explode(":", $_GET["xt"]);
$hash = $e[2];

if(file_put_contents($magnetPath."/meta-".$hash.".torrent", $content)) {
    echo("Torrent written successfully");
} else {
    echo("Error writing torrent");
}
?>
