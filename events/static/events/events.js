/*
    #  here lie our dearest JS functions for
    #  pagination, sorting, and broken image replacement
*/
function imgError(image) {
image.onerror ="";
image.src="http://upload.wikimedia.org/wikipedia/commons/c/c3/Noimage.gif";
image.style="float:left;width:100px;height:100px"
return true;}

var paginationTopOptions = {
    name: "paginationTop",
    paginationClass: "paginationTop",
    outerWindow: 1
  };
var paginationBottomOptions = {
    name: "paginationBottom",
    paginationClass: "paginationBottom",
    outerWindow: 1
  };
var options = {
    valueNames: [ 'name', 'date' ],
    page: 10,
    plugins: [
        ListPagination(paginationTopOptions),
        ListPagination(paginationBottomOptions)
        ]
};

var userList = new List('users', options);