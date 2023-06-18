<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\Cr_Controller;
use App\Http\Controllers\Upload_Controller;
use App\Http\Controllers\Home_Controller;
/*2023/1/9 データベース 接続 */
//use App\Http\Controllers\IndexController;
/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/

Route::get('/', function () {
    return view('welcome');
});

// Route::get('/w\', function () {
//     return view('home');
// });
Route::middleware([
    'auth:sanctum',
    config('jetstream.auth_session'),
    'verified'
])->group(function () {
    Route::get('/dashboard', function () {
        return view('dashboard');
    })->name('dashboard');
    // 追加
    /*
    Route::get('/home', function () {
        return view('home');
    })->name('home');*/

    Route::get('histries', [Home_Controller::class,'index'])->name('home.index');
    Route::get('home_search', [Home_Controller::class,'Search'])->name('home.search');
    Route::get('home_copyright', [Home_Controller::class,'Copyright'])->name('home.copyright');

    /*Route::get('/upload', function () {
        return view('upload');
    })->name('upload');*/
    Route::get('upload', [Upload_Controller::class,'uploadpage'])->name('upload');

    Route::get('/result', function () {
        return view('result');
    })->name('result');
    // 追加
    Route::post('upload',[Upload_Controller::class,'up']);
    Route::get('history_result',[Home_Controller::class,'History'])->name('history');


});

/*Route::middleware([
    'auth:sanctum',
    config('jetstream.auth_session'),
    'verified'
])->group(function () {
    Route::get('/dashboard', [Cr_Controller::class,'index'])->name('dashboard');
});*/

Route::get('/Cr',[Cr_Controller::class,'index']);
//Route::get('/uploadpage',[upload_Controller::class,'uploadpage']);
