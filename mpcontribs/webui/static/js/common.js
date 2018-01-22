requirejs.config({
  baseUrl: 'static/js/lib',
  paths: {
    app: '../app',
    bootstrap: 'bootstrap.min',
    filestyle: 'bootstrap-filestyle.min',
    chosen: 'chosen.jquery.min',
    waitfor: 'jquery.waitFor',
    thebe: 'main-built',
    toggle: 'bootstrap-toggle',
    plotly: "plotly.min",
    underscore: "underscore-min",
    backbone: "backbone-min",
    "backgrid-paginator": "backgrid.paginator"
  },
  shim: {
    bootstrap: { deps: ['jquery'] },
    thebe: { deps: ['jquery'] },
    filestyle: { deps: ['bootstrap'] },
    chosen: { deps: ['jquery', 'bootstrap'] },
    waitfor: { deps: ['jquery'] },
    sandbox: { deps: ['archieml'] },
    toggle: { deps: ['jquery', 'bootstrap'] },
    backgrid: {deps: ['backbone'], exports: 'Backgrid'},
    underscore: {exports: '_'},
    toggle: {deps: ['jquery', 'bootstrap']},
    'backgrid-filter': {deps: ['backgrid']},
    'backbone.paginator': {deps: ['backbone']},
    'backgrid-paginator': {deps: ['backgrid', 'backbone.paginator']},
    'backgrid-grouped-columns': {deps: ['backgrid']},
    'backgrid-patch': {deps: ['backgrid-grouped-columns']},
  }
});
