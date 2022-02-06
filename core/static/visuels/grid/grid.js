//-------------------------------------//

let grid = document.querySelector('.grid');

let msnry = new Masonry( grid, {
  itemSelector: 'none', // select none at first
  columnWidth: '.grid__col-sizer',
  gutter: '.grid__gutter-sizer',
  horizontalOrder: true,
  percentPosition: true,
  stagger: 30,
  // nicer reveal transition
  visibleStyle: { transform: 'translateY(0)', opacity: 1 },
  hiddenStyle: { transform: 'translateY(100px)', opacity: 0 },
});


// initial items reveal
imagesLoaded( grid, function() {
  grid.classList.remove('are-images-unloaded');
  msnry.options.itemSelector = '.grid__item';
  let items = grid.querySelectorAll('.grid__item');
  msnry.appended( items );
});


function getPath() {
    return '/grid/'+ (2+this.loadCount);
}

//-------------------------------------//
// init Infinte Scroll

let infScroll = new InfiniteScroll( grid, {
  path: getPath,
  append: '.grid__item',
  outlayer: msnry,
  status: '.page-load-status',
});

const copyLink = document.querySelector(".copy-img");

copyLink.addEventListener('click', e => {
  if(e.target.classList.contains('btn-copy')) {
    const link = window.location.origin + e.target.dataset.link;
    e.target.classList.add('copied');
    navigator.clipboard.writeText(link);
    setTimeout(() => {
      e.target.classList.remove('copied');
    }, 1000);
  }
})