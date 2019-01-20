<?php

// Setting
$uploads_dir = './clocks';
$allowed_ext = array('png');

// Clean up variables
$error = $_FILES['myfile']['error'];
$name = $_FILES['myfile']['name'];
$ext = array_pop(explode('.', $name));

// Err Check
if ($error != UPLOAD_ERR_OK) {
    switch($error) {
        case UPLOAD_ERR_INI_SIZE:
        case UPLOAD_ERR_FORM_SIZE:
            echo "File is too large ($error)";
            break;
        case UPLOAD_ERR_NO_FILE:
            echo "File not found. ($error)";
            break;
        default:
            echo "The file was not successfully uploaded. ($error)";
    }
    exit;
}

// Checking extension
if (!in_array($ext, $allowed_ext)) {
    echo "Unacceptable extension.";
    exit;
}

// Move File
move_uploaded_file($_FILES['myfile']['tmp_name'], "$uploads_dir/$name");

// Output file information.
echo "<h2>File information</h2>
        <ul>
            <li>File Name : $name</li>
            <li>Extension : $ext</li>
            <li>File Type : {$_FILES['myfile']['type']}</li>
            <li>File Size : {$_FILES['myfile']['size']} Byte</li>
        </ul>"

?>