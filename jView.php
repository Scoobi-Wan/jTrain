<!DOCTYPE html>
<html>
<head>
<title>jTrain</title>
<link rel="stylesheet" type="text/css" href="jStyles.css">
</head>
<body>
<header>
    <form action="jController.php" method="POST">
        <div class="leftNav">
            <a href="jView.php" class="homeButton">Home</a>
        </div>

        <div class="rightNav">
            <input type='submit' name='SignOut' class='signOutButton' value='Sign Out'/>
        </div>
    </form>
</header>


<div class="loginDiv">
<form action="jController.php" method="POST">

<?php

session_start();

require_once __DIR__ . '\jDatabaseAdaptor.php';


    if (isset($_SESSION['username'])) {
        echo "<div class='welcomeDiv'>Hello, " . $_SESSION['username'] . "</div><br><br>";
        echo "<input type='submit' name='CatTrain' class='CatTrain' value='Train By Category'/><br>";
        echo "<input type='submit' name='RandomCatTrain' class='RandomCatTrain' value='Train By Random Category'/>";
    
    } else {
        echo "<h1>Welcome to jTrain!</h1>";
        echo "<h2>A Jeopardy themed trivia training website.</h2><br>";
        echo "<div class='regSign'>";
        echo "<input type='submit' name='Register' class='registerButton' value='Register'/>";
        echo "<input type='submit' name='SignIn' class='signInButton' value='Sign In'/></div>";
    }



?>

</form>
</div>

</body>
</html>
