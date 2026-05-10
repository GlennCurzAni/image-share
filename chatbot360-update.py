#!/usr/bin/env python3
"""Add read-more collapse feature to Chatbot360 Builder widget."""

# --- 1. Update CSS ---
css_file = '/var/www/chatbot/widget/chatbot.css'
css = open(css_file).read()

css_anchor = '.msg.bot {'
idx = css.find(css_anchor)
if idx == -1:
    print('CSS: FAIL - could not find .msg.bot rule')
else:
    # Find the closing } of .msg.bot
    brace = css.find('}', idx)
    if brace == -1:
        print('CSS: FAIL - could not find closing brace')
    else:
        insert_css = """
.msg.bot.cb-collapsed {
  max-height: 120px;
  overflow: hidden;
  -webkit-mask-image: linear-gradient(to bottom, #000 60%, transparent 100%);
  mask-image: linear-gradient(to bottom, #000 60%, transparent 100%);
}
.cb-read-more {
  background: none;
  border: none;
  color: var(--widget-accent, #e74c3c);
  cursor: pointer;
  font-size: 13px;
  padding: 2px 0 0;
  font-family: inherit;
  font-weight: 600;
}
.cb-read-more:hover { text-decoration: underline; }
"""
        css = css[:brace+1] + '\n' + insert_css + css[brace+1:]
        open(css_file, 'w').write(css)
        print('CSS: OK')

# --- 2. Update JS ---
js_file = '/var/www/chatbot/widget/chatbot.js'
lines = open(js_file).readlines()
out = []
i = 0
fn_done = False

while i < len(lines):
    line = lines[i]

    # Find appendMessage function
    if not fn_done and 'function appendMessage(chatBody, role, text, opts)' in line:
        out.append(line)
        i += 1
        # opts = opts || {};
        out.append(lines[i])
        i += 1
        # var msg = document.createElement("div");
        out.append(lines[i])
        ind = lines[i][:len(lines[i]) - len(lines[i].lstrip())]
        i += 1
        # msg.className = "msg " + ...
        out.append(lines[i])
        i += 1
        # msg.textContent = text;
        out.append(lines[i])
        i += 1
        # chatBody.appendChild(msg);
        # Replace with wrapper approach for bot messages
        original_append = lines[i]  # chatBody.appendChild(msg);
        i += 1
        # Next line: if (role !== "user") {
        if_line = lines[i]

        # Insert wrapper + collapse logic
        out.append(ind + 'var wrapper = document.createElement("div");\n')
        out.append(ind + 'wrapper.appendChild(msg);\n')
        out.append(ind + 'if (role !== "user" && text && text.length > 300) {\n')
        out.append(ind + '  msg.classList.add("cb-collapsed");\n')
        out.append(ind + '  var rb = document.createElement("button");\n')
        out.append(ind + '  rb.className = "cb-read-more";\n')
        out.append(ind + '  rb.textContent = "Read more ▼";\n')
        out.append(ind + '  rb.onclick = function () {\n')
        out.append(ind + '    var exp = msg.classList.toggle("cb-collapsed");\n')
        out.append(ind + '    rb.textContent = exp ? "Read more ▼" : "Show less ▲";\n')
        out.append(ind + '    scrollToBottom(chatBody);\n')
        out.append(ind + '  };\n')
        out.append(ind + '  wrapper.appendChild(rb);\n')
        out.append(ind + '}\n')
        out.append(ind + 'chatBody.appendChild(wrapper);\n')
        # Continue with the if (role !== "user") line
        out.append(if_line)
        fn_done = True
        i += 1
        continue

    out.append(line)
    i += 1

open(js_file, 'w').writelines(out)
print('JS appendMessage:', 'OK' if fn_done else 'FAIL')

if fn_done:
    print('Done! Chatbot360 Builder updated with read-more feature.')
else:
    print('WARNING: JS modification failed.')
