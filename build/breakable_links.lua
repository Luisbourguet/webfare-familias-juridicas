-- LaTeX only: a link whose visible text is itself an address (github.com/..., https://...)
-- is typeset with \nolinkurl, so xurl may break it at a slash instead of letting it
-- run into the margin. DOCX and other outputs are untouched.
function Link(el)
  if FORMAT:match('latex') then
    local txt = pandoc.utils.stringify(el.content)
    if txt:match('^github%.com/') or txt:match('^https?://') then
      return pandoc.RawInline('latex', '\\href{' .. el.target .. '}{\\nolinkurl{' .. txt .. '}}')
    end
  end
end
