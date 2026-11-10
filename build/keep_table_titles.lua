-- 1) Evita que el título de una tabla («Tabla I. …») quede huérfano al pie de página.
-- 2) Pone la Tabla III (diez columnas) en una página apaisada, con su título y su nota de fuente.
local function is_title(b, pat)
  if b.t ~= "Para" then return false end
  local f = b.content[1]
  return f and f.t == "Strong" and pandoc.utils.stringify(f):match(pat)
end

function Pandoc(doc)
  local out, i, bl = {}, 1, doc.blocks
  while i <= #bl do
    local b = bl[i]
    if is_title(b, "^Tabla III%.") then
      table.insert(out, pandoc.RawBlock("latex", "\\begin{landscape}"))
      table.insert(out, b)
      -- tabla y nota de fuente que la siguen
      local j = i + 1
      while j <= #bl and (bl[j].t == "Table" or (bl[j].t == "Para" and pandoc.utils.stringify(bl[j]):match("^Fuente"))) do
        table.insert(out, bl[j]); j = j + 1
      end
      table.insert(out, pandoc.RawBlock("latex", "\\end{landscape}"))
      i = j
    else
      if is_title(b, "^Tabla [IVX]+%.") then
        table.insert(out, pandoc.RawBlock("latex", "\\needspace{10\\baselineskip}"))
      end
      table.insert(out, b); i = i + 1
    end
  end
  doc.blocks = out
  return doc
end
