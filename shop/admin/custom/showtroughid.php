<?php
  $conn = new mysqli("localhost", "root", "", "opencart");

  if($conn->connect_error){
    echo "$conn->connect_error";
  }

  $result = $conn->query("SELECT * FROM troughinfo");

  if($result){
    if($result->num_rows > 0){
      echo "<h1>Trough IDs</h1></br>";
      while($row = $result->fetch_assoc()){
        echo $row['troughid'].'</br>';
      }
    }
    else {
      echo "There are no trough IDs";
    }
  }
  else {
    echo "<h1>Failed to display Trough IDs</h1>";
  }
 ?>
