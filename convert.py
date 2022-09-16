import toml
import json
import re
import urllib.request

themes_content = urllib.request.urlopen("https://raw.githubusercontent.com/Patitotective/ImThemes/main/themes.toml").read()
themes = toml.loads(themes_content.decode('utf-8'))

info = {
	"styles": []
}

for theme in themes["themes"]:
	info["styles"].append({
		"name": theme["name"],
		"author": theme["author"],
		"description": theme["description"],
		"screenshot": "screenshots/" + theme["name"] + ".jpg",
		"style": "styles/" + theme["name"] + ".toml"
	})

	f = open("styles/" + theme["name"] + ".toml", "w")
	f.write("# " + theme["name"] + " by " + theme["author"] + " (" + theme["date"].strftime("%B %d %Y") + ")\n")
	f.write("# " + theme["description"] + "\n")
	f.write("# From https://github.com/Patitotective/ImThemes\n\n")

	f.write("[Style]\n")

	for key, value in theme["style"].items():
		if key == "colors":
			continue

		name = key[0].upper() + key[1:]

		if type(value) == str:
			f.write(name + " = \"" + value + "\"\n")
		else:
			f.write(name + " = " + str(value) + "\n")

	f.write("\n[Colors]\n")

	for key, rgba in theme["style"]["colors"].items():
		name = key[0].upper() + key[1:]

		m = re.match("^rgba\\(([0-9]+), ([0-9]+), ([0-9]+), ([^\\)]+)\\)$", rgba)

		# RGB = 0-255, A = 0-1
		r, g, b, a = int(m[1]), int(m[2]), int(m[3]), float(m[4])

		hexvalue = '#{:02X}{:02X}{:02X}'.format(r, g, b)
		if a < 1:
			hexvalue += '{:02X}'.format(int(a * 255))

		f.write(name + " = \"" + hexvalue + "\"\n")

json.dump(info, open("info.json", "w"), sort_keys=True, indent=2)
