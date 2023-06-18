<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class Cr_Controller extends Controller
{
    public function index(){
        $message = "";
        return view('cr',compact('message'));
    }
}

