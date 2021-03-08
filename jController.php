<?php

// This section represents the controller of the MVC architecture. 

session_start ();

require_once __DIR__ . '\jDatabaseAdaptor.php';


$jDBA = new jDatabaseAdaptor();

if (isset ( $_GET ['todo'] ) && $_GET ['todo'] === 'getRandomCatClues') {
    $arr = $jDBA->getCluesFromRandomCat();
    unset($_GET ['todo']);
    $json_arr = json_encode($arr, true);
    echo $json_arr;

}
 
if (isset ($_POST ['Register'])) {
    header('Location: jRegister.php'); 
}

if (isset ($_POST ['SignIn'])) {
    header('Location: jSignIn.php');
}

if (isset ($_POST ['SignOut'])) {
    unset( $_SESSION ['username']);
    header('Location: jView.php');
}

if (isset ($_POST ['CatTrain'])) {
    $_SESSION ['CatTrain'] = "Yes";
    header('Location: trainByCat.php');
}

if (isset ($_POST ['RandomCatTrain'])) {
    $_SESSION ['RandomCatTrain'] = "Yes";
    header('Location: randomCatTrain.php');
}


if (isset ($_POST['registerUsername'])){ 

    $usr = htmlspecialchars($_POST ['registerUsername']);
    $psw = htmlspecialchars($_POST ['registerPassword']);
    if($jDBA->addUser($usr, $psw) === true) {
        $_SESSION ['username'] = $usr;
        header('Location: jView.php');
    } else {
        $_SESSION ['registrationError'] = "Error creating account. Username may already exist.";
        header('Location: jRegister.php');
    }

}

if (isset ($_POST['signInUsername'])){ 

    $usr = htmlspecialchars($_POST ['signInUsername']);
    $psw = htmlspecialchars($_POST ['signInPassword']);
    if($jDBA->verifyCredentials($usr, $psw) === true) {
        $_SESSION ['username'] = $usr;
        header('Location: jView.php');
    } else {
        $_SESSION ['loginError'] = "Error logging in. Incorrect username or password.";
        header('Location: jSignIn.php');
    }

}

