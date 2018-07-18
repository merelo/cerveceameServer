<?php 
	require 'Database.php'; 
	class Meta {

    		function __construct()
    		{
    		}

		//Selects all beers which has, at least, one 5 stars' rating
		public static function estrellas(){
			$consulta="SELECT m1.marca,m1.nombre,m1.puntuacion FROM transacciones m1 LEFT JOIN transacciones m2 
				ON (m1.idUser=m2.idUser AND m1.marca=m2.marca AND m1.nombre=m2.nombre AND m1.id<m2.id) 
				WHERE m2.id IS NULL AND m1.puntuacion=5";
			$consulta="SELECT cinco.marca,cinco.nombre,COUNT(cinco.marca) as cantidad FROM (SELECT m1.marca,m1.nombre FROM transacciones m1 
				LEFT JOIN transacciones m2 ON (m1.idUser=m2.idUser AND m1.marca=m2.marca AND m1.nombre=m2.nombre AND m1.id<m2.id) 
				WHERE m2.id IS NULL AND m1.puntuacion=5) AS cinco GROUP BY cinco.marca, cinco.nombre";
			try{
				$comando=Database::getInstance()->getDb()->prepare($consulta);
                                $comando->execute(array());
				$nFilas=$comando->rowCount();
				
				$resp='{"0":'.json_encode($comando->fetch(PDO::FETCH_ASSOC),JSON_UNESCAPED_UNICODE);
				for($i=1;$i<$nFilas;$i++){
					$aux=$comando->fetch(PDO::FETCH_ASSOC);
					$aux=json_encode($aux,JSON_UNESCAPED_UNICODE);
					$resp=$resp.',"'.$i.'":'.$aux;
				}
				$resp=$resp.'}';
				$resp='{"tam":"'.$nFilas.'","puntuaciones":'.$resp.'}';
				print $resp;
			}catch (PDOException $e){
                                print -1;
                        }
		}

		//Record a new star rating from a user
		public static function nuevaTransaccion($idUser,$marca,$nombre,$puntuacion,$fechaUsuario){
			$fecha = date('Y-m-d G:i:s');
			$consulta="INSERT INTO transacciones (idUser,marca,nombre,puntuacion,fechaUsuario,fechaServidor) 
				VALUES ('$idUser','$marca','$nombre','$puntuacion','$fechaUsuario','$fecha')";
                        try{
                                $comando=Database::getInstance()->getDb()->prepare($consulta);
                                $comando->execute(array());
                                print json_encode(array('estado'=>'ok'));
                        }catch (PDOException $e){
                                print json_encode(array('estado'=>'error'));
                        }
		}
		
		//Returns all beers rated by an user
		public static function valoraciones($user){
			$consulta="SELECT marca, nombre, puntuacion FROM transacciones WHERE puntuacion>0 and id IN (SELECT MAX(id) FROM transacciones WHERE idUser=? GROUP BY marca,nombre)";
			try{
                                $comando=Database::getInstance()->getDb()->prepare($consulta);
				$comando->execute(array($user));
				$nFilas=$comando->rowCount();
				$resp="";
                                for($i=0;$i<$nFilas;$i++){
                                        $aux=$comando->fetch(PDO::FETCH_ASSOC);
                                        $aux=json_encode($aux, JSON_UNESCAPED_UNICODE);
                                        $resp=$resp.$aux." ";
                                }

                                return $resp;
                        }catch (PDOException $e){
                                print -1;
                        }
		}

		//Selects all beers which has, at least, one 5 stars' rating. Same as estrellas() but with puntuaciones set to 0
		public static function mejor_valoradas(){
                        $consulta="SELECT m1.marca,m1.nombre,m1.puntuacion FROM transacciones m1 LEFT JOIN transacciones m2
                                ON (m1.idUser=m2.idUser AND m1.marca=m2.marca AND m1.nombre=m2.nombre AND m1.id<m2.id)
                                WHERE m2.id IS NULL AND m1.puntuacion=5";
                        $consulta="SELECT cinco.marca,cinco.nombre, IF(0=0, '0.0', '0.0') AS punt FROM (SELECT m1.marca,m1.nombre FROM transacciones m1
                                LEFT JOIN transacciones m2 ON (m1.idUser=m2.idUser AND m1.marca=m2.marca AND m1.nombre=m2.nombre AND m1.id<m2.id)
                                WHERE m2.id IS NULL AND m1.puntuacion=5) AS cinco GROUP BY cinco.marca, cinco.nombre";
                        try{
                                $comando=Database::getInstance()->getDb()->prepare($consulta);
                                $comando->execute(array());
                                $nFilas=$comando->rowCount();

                                $resp='{"0":'.json_encode($comando->fetch(PDO::FETCH_ASSOC),JSON_UNESCAPED_UNICODE);
                                for($i=1;$i<$nFilas;$i++){
                                        $aux=$comando->fetch(PDO::FETCH_ASSOC);
                                        $aux=json_encode($aux, JSON_UNESCAPED_UNICODE);
                                        $resp=$resp.',"'.$i.'":'.$aux;
                                }
                                $resp=$resp.'}';
                                print $resp;
                        }catch (PDOException $e){
                                print -1;
                        }
                }

	}

?>
