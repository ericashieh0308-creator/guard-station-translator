
import tkinter as tk
import sys
import tkinter.font as tkfont

# Receive approved translation and selected language
approved_text = (
    sys.argv[1]
    if len(sys.argv) > 1
    else "No approved translation available."
)

target_language = (
    sys.argv[2]
    if len(sys.argv) > 2
    else "en"
)

# Create visitor display window
window = tk.Tk()
window.title("Guard Station - Visitor Display")
window.geometry("850x450")
window.configure(bg="white")

# Title
title = tk.Label(
    window,
    text="Visitor Information",
    font=("Arial", 24, "bold"),
    bg="white"
)
title.pack(pady=35)

# Configure message display
if target_language == "ar":
    import arabic_reshaper
    from bidi.algorithm import get_display

    message_font = ("Segoe UI", 25)
    font_measure = tkfont.Font(
        family="Segoe UI",
        size=25
    )

    # Wrap original Arabic text before applying RTL
    words = approved_text.split()
    lines = []
    current_line = ""

    for word in words:
        candidate = (
            current_line + " " + word
            if current_line
            else word
        )

        candidate_visual = get_display(
            arabic_reshaper.reshape(candidate),
            base_dir="R"
        )

        if (
            font_measure.measure(candidate_visual) <= 750
            or not current_line
        ):
            current_line = candidate
        else:
            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    # Apply RTL separately to each line
    display_text = "\n".join(
        get_display(
            arabic_reshaper.reshape(line),
            base_dir="R"
        )
        for line in lines
    )

    message_justify = "right"
    message_anchor = "e"

else:
    display_text = approved_text
    message_font = ("Microsoft JhengHei", 25)
    message_justify = "center"
    message_anchor = "center"

# Display approved translation
message = tk.Label(
    window,
    text=display_text,
    font=message_font,
    bg="white",
    fg="black",
    wraplength=750 if target_language != "ar" else 0,
    justify=message_justify,
    anchor=message_anchor
)

message.pack(
    expand=True,
    fill="x",
    padx=50
)

# Close button
close_button = tk.Button(
    window,
    text="Close",
    font=("Arial", 14),
    command=window.destroy
)
close_button.pack(pady=30)

window.mainloop()
