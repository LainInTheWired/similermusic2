<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Auth;


class Home_Controller extends Controller
{
    public function index()
    {
        //$history = new History;
        //$values = History::where('userid', '0');
        //$recodes = History::select('uptitle')->get();
        $values = DB::table('histories')->where('userid',Auth::id())->orderby("created_at","desc")->get();
        // ddd($values);
        return view('home' ,compact('values'));
    }

    public function Search(Request $request)
    {
        // //検索フォームで入力された値を取得する
        // $search = $request->input('search');
        // $select = $request->input('select');
        // // $category = $request->input('button');

        // $query = History::query();
        // if(isset($search)){
        //     if($select != 'All'){
        //         $query->where('uptitle','like','%'.$search.'%')
        //               ->where('copyright','like',$select);
        //     }else{
        //         $query->where('uptitle','like','%'.$search.'%');
        //     }
        // }elseif($select == 'All'){
        //     $query->get();
        // }else{
        //     $query->where('copyright','like',$select);
        // }
        // $histories = $query->paginate(20);
        // // ddd($histories->all());
        $user_id = Auth::id();
        $query = History::query();
        $histories = $query->where('userid',$user_id);
        return view('home', compact('histories'));
    }

    public function History(Request $request){
        $url = $request->input('id');
        $file_name = $request->music;
        // ddd($url);;
        $json = file_get_contents($url);
        $json = mb_convert_encoding($json, 'UTF8', 'ASCII,JIS,UTF-8,EUC-JP,SJIS-WIN');
        $json  = json_decode($json,true);
        foreach($json as $key => $j){
            $sort_keys[$key] = $j['aggregated'];
        }
        array_multisort($sort_keys,$json);
        return( view('result',compact('json','file_name')));
    }
}
