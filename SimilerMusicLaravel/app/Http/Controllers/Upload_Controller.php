<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Str;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Auth;





class Upload_Controller extends Controller
{
    public function uploadpage()
    {
        return view('upload');

    }
    // 追加
    public  function up(Request $request)
    {
        // api受け取り
        $validated = $request->validate([
            's_file' => ['required' , 'mimes:mp3'],
        ]);
        // ddd($request->file('s_file'));
        $file_name = $request->file('s_file')->getClientOriginalName();
        $file_name = str_replace(" ","_",$file_name);
        // ddd($file_name);
        Storage::disk('music') ->putFileAs('',$request->file('s_file'),$file_name);
        $json = Http::get('http://localhost:11000/?id=/root/sim/music/out/'.$file_name);
        // print($json);
        // test用jsonファイル読み込み
        // $url = "sample.json";
        // $json = file_get_contents($url);
        // $json = mb_convert_encoding($json, 'UTF8', 'ASCII,JIS,UTF-8,EUC-JP,SJIS-WIN');
        // json保存
        $path = 'history/'.date("Ymd");
        // ddd(Storage::disk('public')->url($path));
        if(!Storage::disk('app_public')->exists($path)){
            Storage::disk('app_public')->makeDirectory($path);
        }
        // Storage::putFile($json,$path);
        $json_name = $path.'/'.Str::random(30).'.json';
        // ddd($file_name);
        Storage::disk("app_public")->prepend($json_name, $json);


        $json  = json_decode($json,true);
        foreach($json as $key => $j){
            $sort_keys[$key] = $j['aggregated'];
        }
        // ddd(gettype(Auth::id()));
        DB::table('histories')->insert([
            'userid' => Auth::id(),
            'upid' => $file_name,
            'json' => $json_name
        ]);



        array_multisort($sort_keys,$json);
        return view('result' ,compact('json','file_name'));
    }
}
