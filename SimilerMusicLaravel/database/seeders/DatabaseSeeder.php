<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

class DatabaseSeeder extends Seeder
{
    /**
     * Seed the application's database.
     *
     * @return void
     */
    public function run()
    {
        // \App\Models\User::factory(10)->create();
        #データベース追加処理
        DB::transaction(function () {
            DB::table('test')->insert([
                [
                'userid' => 0,
                'uptitle' => 'aa',
                'resulttitle' =>'bb' ,
                'auther' => 'cc',
                'similarity' => 95,
                'bpm' => 75,
                'copyright' => 'free'
                ]
            ]);
        });
    }
}
