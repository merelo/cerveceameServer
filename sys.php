<?php
header('Content-Type: text/html; charset=UTF-8');
$iduser=htmlspecialchars($_GET["iduser"]);
require 'Meta.php';
$valor=Meta::valoraciones($iduser);
if(empty($valor)){
  $output = Meta::mejor_valoradas();
}else
  $output = exec('python /var/www/cerveceame/server/recsys.py '.$valor.' 2>&1');

echo $output;
?>
