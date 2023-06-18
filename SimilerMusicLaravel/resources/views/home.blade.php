<x-app-layout>
    <h2 class="font-medium leading-tight text-4xl mt-0 mb-4 text-black">history</h2>
    <ol class="relative border-l border-gray-200 dark:border-gray-700">
        @foreach ($values as $value)
            <li class="mb-10 ml-4">
                <div class="absolute w-3 h-3 bg-gray-200 rounded-full mt-1.5 -left-1.5 border border-white dark:border-gray-900 dark:bg-gray-700"></div>
                <time class="mb-1 text-sm font-normal leading-none text-gray-400 dark:text-gray-500">{{$value->created_at}}</time>
                <h3 class="text-lg font-semibold text-gray-900 dark:text-white"><a href="{{ route('history',['id' => $value->json,'music' => $value->upid]) }}">{{$value->upid}}<a></h3>
            </li>
        @endforeach
    </ol>
</x-app-layout>

