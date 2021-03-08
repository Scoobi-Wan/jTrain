  
<!DOCTYPE html>
<html>
<head>
<title>Sign In</title>
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
<div class="signInContainer">
<h3>Please sign in.</h3>
<div class="signInFormDiv">
    <input type="text" name="signInUsername" placeholder='Username' required>
    <br>
    <input type="password" name="signInPassword" placeholder='Password' required>
    <br><br>
    <input type="submit" value="Sign In"> <br>
    <div id="loginFailDiv"></div>

<?php 
if( isset($_SESSION ['loginError']))
  echo $_SESSION ['loginError']; 
unset($_SESSION ['loginError']);


?>

</div>

</form>
</body>
</html>
