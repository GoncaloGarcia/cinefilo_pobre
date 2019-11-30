var csvarray;
var channels;
d3.text("out.csv", function(data) {
	var parsedCSV = d3.csv.parseRows(data);
	csvarray = parsedCSV;
	channels = new Set(csvarray.map(arr => arr[2])
		.map(value => value.split(","))
		.flat()
		.map(str => str.trim()))
	d3.select("tbody")
		.selectAll("tr")
		.data(csvarray)
		.enter()
		.append("tr")
		.selectAll("td")
		.data(function(d) { return d; }).enter()
		.append("td")
		.attr("align", "center")
		.attr("valign", "middle")
		.text(function(d) { return d; });
	d3.select(".dropdown-menu")
		.selectAll(".dropdown-content")
		.data([...channels])
		.enter().append("div")
		.attr("class", "dropdown-content")
		.append("input")
		.attr("type", "checkbox")
		.on("change", function() {
		//	console.log(d3.selectAll("input").select(this.parentNode).select("label").text());
		});
	d3.select(".dropdown-menu")
		.selectAll(".dropdown-content")
		.append("label")
		.attr("class", "checkbox")
		.text(function (e) { return "  " + e; });
});

d3.select("#sortAscending")
	.on("click", function() {
		var tablemy = d3.select("tbody").selectAll("tr").data(csvarray.reverse());
		var elements = tablemy.selectAll("td").data(function(d) { return d; });
		elements.text(function(d) { return d; });
	});

