let getTooltip = function(column){
  let d = column.getDefinition().description;
  if (d) {
    return d
  }

  return false
}

table = new Tabulator("#models-table", {

  // Data
  ajaxURL: "models/models.json",
  ajaxContentType: "json",
  ajaxResponse: function(url, params, response){
    return response;
  },

  // Formatting
  columns: [
    {title:"Model Name", field:"name", responsive: 0, widthGrow: 2, minWidth: 150},
    {title:"Dataset", field:"dataset", responsive: 0, widthGrow: 2, minWidth: 150},
    {
      title:"Score",
      field:"haddock_score",
      description:"HADDOCK score. A prediction of how well the proteins interact. Lower scores mean stronger (better) interactions.",
      responsive: 0,
      minWidth: 100
    },
    {
      title:"vdW",
      field:"e_vdw",
      minWidth: 75,
      description:"van der Waals energy of the interface in kcal/mol. Lower is better.",
    },
    {
      title:"Electrostatics",
      field:"e_elec",
      minWidth: 75,
      description:"Electrostatic energy of the interface in kcal/mol. Lower is better.",
    },
    {
      title:"Desolvation",
      field:"e_desolv",
      minWidth: 75,
      description:"Empirical desolvation energy of the interface. Lower is better.",
    },
    {
      title:"BSA",
      field:"buried_surf_area",
      minWidth: 75,
      description:"Buried Surface Area in sq A.",
    },
  ],

  // Layout
  layout:"fitColumns",
  resizableColumns: false,
  selectable: true,
  columnHeaderVertAlign: "bottom", //align header contents to bottom of cell
  responsiveLayout: "hide",

  tooltipsHeader: getTooltip,
  // pagination: "local",
  // paginationSize: 10,  // model per page.

    // Callbacks
  rowSelected:function(row){
    let pdburl = "models/" + row.getData().url;
    let pdbname = row.getData().name;
    loadMolecule(stage, pdburl)
  },

  rowDeselected:function(row){
    let pdburl = "models/" + row.getData().url;
    let pdbname = row.getData().name;
    removeMolecule(stage, pdburl)
  },

});
