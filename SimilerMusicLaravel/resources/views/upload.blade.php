<x-app-layout>
    <div id="updoze" class="py-12  px-3.5 max-w-7xl mx-auto sm:px-6 lg:px-8 ">
        <p class="text-3x1">MP3File Upload</p>
        <form method="POST" action="/upload" enctype="multipart/form-data">
        @csrf
            <div class="text-center border-2">
                <img src="/images/upload.png" class="inline p-10 m-auto w-1/5 h-full">
                <p>Drag & Drop</p>
                <!-- <button class="border w-32 h-11 text-white bg-gray-600">Select files</button> -->
                <div>
                <input id="fileinput"class=" text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400" type = "file" name = "s_file" multiple>
                </div>
                {{-- <div ><input class="border-2 border-black" type = "file" name = "s_file"></div> --}}
                {{-- 追加 --}}
                @error('s_file')
                    <p>{{$message}}</p>
                @enderror
                <button id="submit" class="bg-transparent hover:bg-white text-black font-semibold my-2 px-4 border border-slate-500  rounded">
                    送信
                </button>

                {{-- <button type="submit">送信</button> --}}
            <!-- <a class=" flex border  w-32 h-11 text-white bg-gray-600" href=" {{ route('result') }}">Select files</a>-->
            </div>
        </form>
        <div id="loading" class="flex justify-center my-20 space-x-3" >
            <div class="animate-ping  h-2 w-2 bg-blue-600 rounded-full"></div>
            <div class="animate-ping  h-2 w-2 bg-blue-600 rounded-full animation-delay-200"></div>
            <div class="animate-ping  h-2 w-2 bg-blue-600 rounded-full animation-delay-400"></div>
        </div>
    </div>
    <script src="{{ mix('js/upload.js') }}"><script>

</x-app-layout>



