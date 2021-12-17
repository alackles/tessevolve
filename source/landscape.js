var accessor = function(row) {
    return {
        x: +row.x*10,
        y: +row.y*10,
        z: +row.z*10,
        fitness: +row.fitness,
        id: +row.id
    }
}

// remove this
// make a new function that turns the lod file into a single string
// once you've done that, put it in meshline
// and you should be good to go


var coords = function(x, y, z) {
    return x + " " + y + " " + z
}

var load_landscape = function(filename1, filename2) {

    var scene = d3.select('a-scene')

    Promise.all([
        d3.csv(filename1, accessor),
        d3.csv(filename2, accessor),
    ])
    .then(
        function(files) {
        landscape = files[0]
        lod = files[1]

        var pts = scene.selectAll('a-sphere')
            .data(landscape, function(d){return d.x})
        
        var nodes = scene.selectAll('a-box')
            .data(lod, function(d){return d.id})

        var min = d3.min(landscape, function(d) {return d.fitness});
        var max = d3.max(landscape, function(d) {return d.fitness});

        var colScale = d3.scaleSequential(d3.interpolatePlasma);
        colScale.domain([min, max])

        pts.enter()
            .append('a-sphere')
            .attr('class', 'data_point')
            .attr('color', function(d) {return colScale(d.fitness)})
            .attr('position', function(d) {return coords(d.x, d.y, d.z)})
            .attr('radius', 1)
            .attr('opacity', 0.9);

        nodes.enter()
            .append('a-box')
            .attr('class', 'phylo_node')
            .attr('color', '#000')
            .attr('position', function(d) {return coords(d.x1, d.y1, d.z1)})

        }
    )

}



