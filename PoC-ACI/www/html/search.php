<?php 
//load database connection
    $host = "localhost";
    $user = "root";
    $password = "redhat";
    $database_name = "apic";
    $pdo = new PDO("mysql:host=$host;dbname=$database_name", $user, $password, array(
    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION
    ));
// Search from MySQL database table
$search=$_POST['search'];
$query = $pdo->prepare("select * from epgport where epg LIKE '%$search%' OR name LIKE '%$search%'");
$query->bindValue(1, "%$search%", PDO::PARAM_STR);
$query->execute();
// Display search result
         if (!$query->rowCount() == 0) {
//		echo"<style>table {border-collapse: collapse;width: 100%;}"
//		echo"th, td {padding: 8px;text-align: left;border-bottom: 1px solid #ddd;}"
//		echo"tr:hover{background-color:#f5f5f5}</style>"
 		echo "Search result :<br/>";
		echo "<table style=\"border-collapse: collapse;width: 100%;\">";	
                echo "<tr style=\"hover{background-color:#f5f5f5;\"><td style=\"padding: 8px;text-align: left;border-bottom: 1px solid #ddd;\"><b>Tenant</b></td><td style=\"padding: 8px;text-align: left;border-bottom: 1px solid #ddd;\"><b>Application Profile</b></td><td style=\"padding: 8px;text-align: left;border-bottom: 1px solid #ddd;\"><b>EPG</b></td><td style=\"padding: 8px;text-align: left;border-bottom: 1px solid #ddd;\"><b>Interface Group</b></td><td style=\"padding: 8px;text-align: left;border-bottom: 1px solid #ddd;\"><b>Interface Profile</b></td><td style=\"padding: 8px;text-align: left;border-bottom: 1px solid #ddd;\"><b>Port</b></td></tr>";
            while ($results = $query->fetch()) {
				echo "<tr><td style=\"padding: 8px;text-align: left;border-bottom: 1px solid #ddd;\">";			
                echo $results['tenant'];
				echo "</td><td style=\"padding: 8px;text-align: left;border-bottom: 1px solid #ddd;\">";
                echo $results['app'];
				echo "</td><td style=\"padding: 8px;text-align: left;border-bottom: 1px solid #ddd;\">";
                echo $results['epg'];
				echo "</td><td style=\"padding: 8px;text-align: left;border-bottom: 1px solid #ddd;\">";
                echo $results['name'];
				echo "</td><td style=\"padding: 8px;text-align: left;border-bottom: 1px solid #ddd;\">";
                echo $results['intprof'];
				echo "</td><td style=\"padding: 8px;text-align: left;border-bottom: 1px solid #ddd;\">";
                echo $results['interface'];
				echo "</td></tr>";				
            }
				echo "</table>";		
        } else {
            echo 'Nothing found';
        }
?>
