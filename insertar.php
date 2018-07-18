<?php
    require 'Meta.php';
	header('Content-Type: text/html; charset=UTF-8');	
	$idUser=htmlspecialchars($_GET["iduser"]);
	$marca=htmlspecialchars($_GET["marca"]);
	$nombre=htmlspecialchars($_GET["nombre"]);
	$puntuacion=htmlspecialchars($_GET["puntuacion"]);
	$fechaUsuario=htmlspecialchars($_GET["fechausuario"]);
	$marca=str_replace("'","\'",$marca);
	$nombre=str_replace("'","\'",$nombre);
	Meta::nuevaTransaccion($idUser,$marca,$nombre,$puntuacion,$fechaUsuario);
?>
