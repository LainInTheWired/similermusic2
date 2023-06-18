{{-- 追加 --}}
<x-app-layout>
    <x-list-music :music="$json">
         <x-slot name="filename">
            <h2 class="text-4xl font-bold dark:text-white ">{{$file_name}}</h2>
         </x-slot>
    </x-list-music>
</x-app-layout>
