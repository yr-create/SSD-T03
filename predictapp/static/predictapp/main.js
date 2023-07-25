const url = "/static/predictapp/Json/2023-07.json";	// JSONファイル名
let result;

// JSONファイルを整形して表示する
function formatJSON(data){
	// 整形して表示
	let html = "<table>";
	html += "<caption>" + data.caption + "</caption>";
    let number = 1;
	for(let member of data.members){
		html += "<tr><td>" + String(number) + "</td><td>"+ member.name + "</td><td>" + String(member.sales) + "</td></tr>";
        number++;
	}
	html += "</table>";

	html += "<p>ぜんぶで" + data.members.length + "種類" + "</p>";	// 要素memberの配列要素数

	result.innerHTML = html;
	
}

// 起動時の処理
window.addEventListener("load", ()=>{
	// JSON表示用
	result = document.getElementById("result");

	// JSONファイルを取得して表示
	fetch(url)
		.then( response => response.json())
		.then( data => formatJSON(data));

});