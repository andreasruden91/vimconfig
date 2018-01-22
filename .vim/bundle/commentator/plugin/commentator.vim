if !has('python')
    finish
endif

if exists("g:loaded_commentator")
  finish
endif
let g:loaded_commentator = 1

function Commentator_cstyle() range
    pyfile ~/.vim/bundle/commentator/plugin/commentator_cstyle.py
endfunc

vnoremap gc :call Commentator_cstyle()<CR>
