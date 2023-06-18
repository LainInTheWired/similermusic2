const { list } = require("postcss");

{
    console.log(music);
    console.log(location.pathname);
    let page = 1; // 現在のページ（何ページ目か）
    const step = 20; // ステップ数（1ページに表示する項目数）

    let musiclist = music

    const form = document.getElementById('form-music-search')
    form.onsubmit = () =>  {return false}

    var table = document.getElementById('music-table')

    createTable(music,page,step)

    for (var item of document.getElementById('page').children){
        console.log(item.textContent)
        item.addEventListener("click",function fn() {
            var maxPage = Math.ceil(musiclist.length/step)
            page = Number(this.textContent)
            // console.log(page)
            let i = page -2
            console.log(page + 2)
            if(maxPage  <= page +2){
                i = maxPage -5
            }else if(page  < 3){
                i = 1
            }
            if(maxPage < 5){i = 1}
            console.log("maxpage" + maxPage)
            for (var item of document.getElementById('page').children){
                item.textContent = i
                if(i == page){
                    item.setAttribute('class','z-10 px-3 py-2 leading-tight text-blue-600 border border-blue-300 bg-blue-50 hover:bg-blue-100 hover:text-blue-700 dark:border-gray-700 dark:bg-gray-700 dark:text-white')
                }else{
                    item.setAttribute('class','px-3 py-2 leading-tight text-gray-500  border border-gray-300 hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white')
                }
                i++
            }
            createTable(musiclist,page,step)
            window.scroll({top:0})

        })
    }

    //検索処理
    document.getElementById("button").onclick = () => {
        while( table.rows[ 1] ) table.deleteRow( 1 );
        console.log("onclick")
        page = 1
        const text = document.getElementById("search-input").value
        const type = document.getElementById("search-select").value

        musiclist = music
        console.log(type)
        switch(type){
            case 'Free':
                musiclist =  music.filter(e => {
                    if( e['id'].indexOf('/root/sim/music/out') == -1){
                        return true
                    }
                })
            break
            case 'NotFree':
                musiclist = music.filter(e => {
                    if( e['id'].indexOf('/root/sim/music/out') != -1){
                        return true
                    }
                })
            break;
        }
        musiclist = musiclist.filter(e => {
            if(e["id"].indexOf(text) != -1){
                return true
            }
        })
        let i=1
        for (var item of document.getElementById('page').children){
            item.textContent = i
            if(i == page){
                item.setAttribute('class','z-10 px-3 py-2 leading-tight text-blue-600 border border-blue-300 bg-blue-50 hover:bg-blue-100 hover:text-blue-700 dark:border-gray-700 dark:bg-gray-700 dark:text-white')
            }else{
                item.setAttribute('class','px-3 py-2 leading-tight text-gray-500  border border-gray-300 hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white')
            }
            i++
        }
        console.log(musiclist)
        createTable(musiclist,page,step)
    }
    function createTable(music,page,step){
        // 一度リストを空にする
        while( table.rows[ 1] ) table.deleteRow( 1 );
        const first = (page - 1) * step + 1;
        const last = page * step;
        music.forEach((e,i) => {
            if(i < first - 1 || i > last - 1) return
            var tr = document.createElement('tr')
            var tdid = document.createElement('td')
            var tdartist = document.createElement('td')
            var tdagg = document.createElement('td')
            var tdbpm = document.createElement('td')
            var tdcopy = document.createElement('td')
            var a = document.createElement('a')
            const id = e['id'].split('/')
            const idText = id.slice(-1)[0].replace("mp3","")
            // const idText = e["id"]
            if( e['id'].indexOf('/root/sim/music/out') == -1){
                tdcopy.innerHTML = 'o'
                a.innerHTML = idText
                a.setAttribute('style', "text-decoration:underline;text-decoration-color: black;")
                a.setAttribute('href', e["url"])
                a.setAttribute('target', "_blank")
                tdid.appendChild(a)
            }else{
                tdcopy.innerHTML = 'x'
                tdid.innerHTML = idText
            }
            tr.appendChild(tdid);
            tdartist.innerHTML = e['artist']
            tr.appendChild(tdartist);
            tdagg.innerHTML = e['aggregated']
            tr.appendChild(tdagg);
            tdbpm.innerHTML = e['bpm']
            tr.appendChild(tdbpm);

            tr.appendChild(tdcopy);
            table.appendChild(tr)
        });
    }
}
