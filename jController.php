<?php

// This section represents the controller of the MVC architecture. 

session_start ();

require_once './jDatabaseAdaptor.php';

$jDBA = new jDatabaseAdaptor();
 

if (isset ($_POST ['username'])) {
    
    $usr = htmlspecialchars($_POST ['username']);
    $psw = htmlspecialchars($_POST ['password']);
    if ($jDBA->verifyCredentials($usr, $psw) === true) {
        $_SESSION ['username'] = $usr;
        header('Location: jView.php');
    } else {
        $_SESSION ['loginError'] = "Incorrect username or password. Please try again.";
        header('Location: jView.php');
    }
    //$jDBA->verifyCredentials;
}

if (isset ($_POST ['Register'])) {
    header('Location: jRegister.php'); 
}

if (isset ($_POST ['registerUsername']) && isset ($_POST ['registerPassword'])) {
    $usrID = htmlspecialchars($_POST ['registerUsername']);
    $usrPwd = htmlspecialchars($_POST ['registerPassword']);
    if ($jDBA->addUser($usrID, $usrPwd) === true) {
        header('Location: jView.php');
    } else {
        $_SESSION['registrationError'] = "Account name taken";
        header('Location: jRegister.php');
    }
}
