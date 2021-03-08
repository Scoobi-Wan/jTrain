  
<!DOCTYPE html>
<html>
<head>
<title>Register</title>
<link rel="stylesheet" type="text/css" href="jStyles.css">
<!-- Author: Paul Rich -->
</head>
<body>
    <header>
        <div class="leftNav">
            <a href="jView.php" class="homeButton">Home</a>
        </div>
</header>


<?php session_start() ?>

<h1>Welcome to jTrain!</h1>
<h2>A Jeopardy themed trivia training website.</h2>
<form autocomplete="off"  action="jController.php" method="post">
<div class="registerContainer">
<h3>Registration</h3>
<div class="registerFormDiv">
    <input type="text" name="registerUsername" placeholder='Username' required>
    <br>
    <input type="password" name="registerPassword" placeholder='Password' required>
    <br><br>
    <input type="submit" value="Register"> <br>
    <div id="nameTakenDiv"></div>

<?php 
if( isset($_SESSION ['registrationError']))
  echo $_SESSION ['registrationError']; 
unset($_SESSION ['registrationError']);


?>

</div>

</form>
</body>
</html>
