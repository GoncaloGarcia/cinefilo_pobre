var csvarray;
var channels;
var exclusions;
var allrows;
var alldata;
var order = true;

d3.text("out.csv", function(data) {
	d3.csv("exclusions.csv", function(exclusions) {
		exclusions = exclusions.map(Object.values).map(item => JSON.stringify(item));
		var parsedCSV = d3.tsv.parseRows(data);
		csvarray = parsedCSV.filter(item => !exclusions.includes(JSON.stringify([item[0],item[2]])));
		alldata=[...csvarray];
		channels = new Set(csvarray.map(arr => arr[2])
			.map(value => value.split(","))
			.flat()
			.map(str => str.trim()).map(str => str.split("<br>")[0]));
		d3.select("tbody")
			.selectAll("tr")
			.data(csvarray, function(d) { return d; })
			.enter()
			.append("tr")
			.selectAll("td")
			.data(function(d) { return d; }).enter()
			.append("td")
			.attr("align", "center")
			.attr("vertical-align", "middle")
			.html(function(d) { 
				if (d.startsWith("(")) {
					var replaced = d.replace(/\(|\)/g, "").split("-");
					var toPrint = "";
					for (var item in replaced) {
						var splitItems = replaced[item].split(",");
						toPrint += "<a href=https://www.imdb.com/title/" +  splitItems[1] +  ">" + splitItems[0] + "</a> | "
					}
					return toPrint.slice(0, -3);
				}
				return d; 
			});
		d3.select(".dropdown-menu")
			.selectAll(".dropdown-content")
			.data([...channels])
			.enter().append("div")
			.attr("class", "dropdown-content")
			.append("input")
			.attr("type", "checkbox")
			.property("checked", "true")
			.on("change", function() {
				var filtered = d3.selectAll("input")[0].filter(item => item["checked"] === true).map(item => item.__data__);
				csvarray = [...alldata];
				console.log(csvarray);
				csvarray = csvarray.filter(item => filtered.includes(item[2].split("<br>")[0]));
				console.log(csvarray);
				var rows = d3.select("tbody")
					.selectAll("tr")
					.data(csvarray, function (d) { return d;});
				allrows = rows;
				rows.exit().remove();
				rows.enter()
					.append("tr")
					.selectAll("td")
					.data(function(d) { return d; }).enter()
					.append("td")
					.attr("align", "center")
					.attr("vertical-align", "middle")
					.html(function(d) {
						if (d.startsWith("(")) {
							var replaced = d.replace(/\(|\)/g, "").split("-");
							var toPrint = "";
							for (var item in replaced) {
								var splitItems = replaced[item].split(",");
								toPrint += "<a href=https://www.imdb.com/title/" +  splitItems[1] +  ">" + splitItems[0] + "</a> | "
							}
							return toPrint.slice(0, -3);
						}
						return d;
					});
				rows.order();

			});
		d3.select(".dropdown-menu")
			.selectAll(".dropdown-content")
			.append("label")
			.attr("class", "checkbox")
			.text(function (e) { return "  " + e; });
	});
});

	d3.select("#sortAscending")
		.on("click", function() {
			var button = d3.select("#sortAscending").select(".la");
			if (order){
				order = !order;
				button.attr("class", "la la-sort-numeric-up");
			}
			else {
				order = !order;
				button.attr("class", "la la-sort-numeric-down-alt");	
			}
			var tablemy = d3.select("tbody").selectAll("tr").data(csvarray.reverse());
			var elements = tablemy.selectAll("td").data(function(d) { return d; });
			elements.html(function(d) {
				if (d.startsWith("(")) {
					var replaced = d.replace(/\(|\)/g, "").split("-");
					var toPrint = "";
					for (var item in replaced) {
						var splitItems = replaced[item].split(",");
						toPrint += "<a href=https://www.imdb.com/title/" +  splitItems[1] +  ">" + splitItems[0] + "</a> | "
					}
					return toPrint.slice(0, -3);
				}
				return d; 
			});
		});

