<!DOCTYPE html>
<html>
<head>
<title>jTrain</title>
<link rel="stylesheet" type="text/css" href="jStyles.css">
</head>
<body onload="showQuotes()">
<h1>Welcome to jTrain!</h1>
<h2>A Jeopardy themed trivia training website.</h2>
<br>

<div class="loginDiv">
<form action="controller.php" method="POST">

<?php
echo "<input type='submit' name='Login' class='loginButton' value='Login'/>";

?>

</form>
</div>
</body>
</html>
