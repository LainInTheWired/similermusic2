<?php

namespace App\View\Components;

use Illuminate\View\Component;

class ListMusic extends Component
{
    /**
     * Create a new component instance.
     *
     * @return void
     */
    public $music;
    public function __construct($music)
    {
        //
        $this->music = $music;
    }

    /**
     * Get the view / contents that represent the component.
     *
     * @return \Illuminate\Contracts\View\View|\Closure|string
     */
    public function render()
    {
        return view('components.list-music');
    }
}
