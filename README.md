# deadline-clock
A tiny CLI that calculates appeal deadlines based on procedural codes. Feed it a code and a starting date, and it’ll spit out a table with every relevant deadline.

It also shows how many days you’ve got left, and turns the progress bar red when you’re cutting it close.

Figured someone else might find it handy too. 🤝

# setup
git clone https://github.com/yourusername/deadline-clock.git
cd deadline-clock
pip install -r requirements.txt

## Usage

python clock.py АПК 15.01.2025

Dates are easy — `15.01.2025`, `2025-01-15`, `15.01.25` all work.

## Codes supported

- ГПК: appeal 1 month, cassation +3, supervisory +3
- АПК: appeal 1 month, cassation +2, supervisory +3
- КАС: appeal 1 month, cassation +6, supervisory +3
- УПК: cassation +6, supervisory +12
