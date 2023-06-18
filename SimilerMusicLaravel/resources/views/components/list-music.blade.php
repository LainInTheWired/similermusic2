<style>
    @media screen and (max-width:480) {

    }
    th,td {
        border: solid 1px rgb(155, 154, 154);
        padding: 13px;
        color:rgb(75 85 99);
    }
</style>
<div class="container font-light mx-auto flex justify-between">
    {{-- <form method="GET" action="{{ route('home.search')}}" id='form-music-search'> --}}
    {{-- <h1 class="">{{$m }}</h1> --}}
    {{$filename }}
    <form method="GET" id='form-music-search' >
        <div class="flex flex-wrap">
            <input id="search-input" type="search"  placeholder="Serch" name="search" value="@if (isset($search)) {{$search}} @endif" class="w-80">
            <select id="search-select" name="select">
                <option  value="All">ALL</option>
                <option value="Free">FREE</option>
                <option value="NotFree">NotFree</option>
            </select>
            <button id="button" type="submit" class="h-11 w-11 align-middle bg-gray-600 ml-auto mr-auto "><img src="/images/serch_1.png" class="h-5 w-5 mr-auto ml-auto "></button>
        </div>
    </form>
</div>
<table  class=" mt-5 w-full content-center">
    <tbody id="music-table">
        <tr><th>Title</th><th>Author</th><th>similarity</th><th>BPM</th><th>Copyright</th></tr>
    </tbody>
</table>
{{-- ページネーション --}}
<nav aria-label="Page navigation example" class="mt-6 ">
    <ul id="page" class=" items-center -space-x-px flex justify-center">
        <li class="z-10 px-3 py-2 leading-tight text-blue-600 border border-blue-300 bg-blue-50 hover:bg-blue-100 hover:text-blue-700 dark:border-gray-700 dark:bg-gray-700 dark:text-white">1</li>
        <li class="px-3 py-2 leading-tight text-gray-500  border border-gray-300 hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">2</li>
        <li class="px-3 py-2 leading-tight text-gray-500  border border-gray-300 hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">3</li>
        <li class="px-3 py-2 leading-tight text-gray-500  border border-gray-300 hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">4</li>
        <li class="px-3 py-2 leading-tight text-gray-500  border border-gray-300 hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">5</li>
    </ul>
</nav>

<script>
    const music = @json($music)
</script>
<script src="{{ mix('js/music-list.js') }}"><script>
