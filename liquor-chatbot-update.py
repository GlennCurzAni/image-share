#!/usr/bin/env python3
"""Add read-more collapse feature to LiquorOnline chat widget."""

f = '/opt/liquor-chatbot/static/index.html'
lines = open(f).readlines()
out = []
i = 0
css_done = fn_done = False

while i < len(lines):
    line = lines[i]

    # 1. CSS: insert after .lo-msg.bot { ... } closing brace
    if not css_done and '.lo-msg.bot {' in line and '.lo-msg-bubble' not in line:
        out.append(line)
        i += 1
        while i < len(lines):
            out.append(lines[i])
            if lines[i].strip() == '}':
                break
            i += 1
        ind = lines[i][:len(lines[i]) - len(lines[i].lstrip())]
        out.append(ind + '.lo-msg.bot.lo-collapsed .lo-msg-bubble {\n')
        out.append(ind + '  max-height: 120px;\n')
        out.append(ind + '  overflow: hidden;\n')
        out.append(ind + '  -webkit-mask-image: linear-gradient(to bottom, #000 60%, transparent 100%);\n')
        out.append(ind + '  mask-image: linear-gradient(to bottom, #000 60%, transparent 100%);\n')
        out.append(ind + '}\n')
        out.append(ind + '.lo-read-more {\n')
        out.append(ind + '  background: none;\n')
        out.append(ind + '  border: none;\n')
        out.append(ind + '  color: #d4af37;\n')
        out.append(ind + '  cursor: pointer;\n')
        out.append(ind + '  font-size: 13px;\n')
        out.append(ind + '  padding: 2px 0 0;\n')
        out.append(ind + '  font-family: inherit;\n')
        out.append(ind + '  font-weight: 600;\n')
        out.append(ind + '}\n')
        out.append(ind + '.lo-read-more:hover { text-decoration: underline; }\n')
        css_done = True
        i += 1
        continue

    # 2. JS: modify addMessage to add collapse for long bot messages
    if not fn_done and 'function addMessage(text, sender)' in line:
        out.append(line)
        i += 1
        # Collect lines until messagesEl.appendChild(div);
        while i < len(lines):
            if 'messagesEl.appendChild(div)' in lines[i]:
                ind = lines[i][:len(lines[i]) - len(lines[i].lstrip())]
                # Insert wrapper logic before appendChild
                out.append(ind + "const msgWrap = document.createElement('div');\n")
                out.append(ind + 'msgWrap.appendChild(div);\n')
                out.append(ind + "if (sender === 'bot' && text && text.length > 300) {\n")
                out.append(ind + "  div.classList.add('lo-collapsed');\n")
                out.append(ind + "  const rb = document.createElement('button');\n")
                out.append(ind + "  rb.className = 'lo-read-more';\n")
                out.append(ind + "  rb.textContent = 'Read more ▼';\n")
                out.append(ind + '  rb.onclick = function () {\n')
                out.append(ind + "    const exp = div.classList.toggle('lo-collapsed');\n")
                out.append(ind + "    rb.textContent = exp ? 'Read more ▼' : 'Show less ▲';\n")
                out.append(ind + '    scrollToBottom();\n')
                out.append(ind + '  };\n')
                out.append(ind + '  msgWrap.appendChild(rb);\n')
                out.append(ind + '}\n')
                out.append(ind + 'messagesEl.appendChild(msgWrap);\n')
                fn_done = True
                i += 1
                continue
            out.append(lines[i])
            i += 1
        continue

    out.append(line)
    i += 1

open(f, 'w').writelines(out)
print('CSS:', 'OK' if css_done else 'FAIL')
print('addMessage:', 'OK' if fn_done else 'FAIL')
if css_done and fn_done:
    print('Done! LiquorOnline chatbot updated with read-more feature.')
else:
    print('WARNING: Some modifications failed.')
