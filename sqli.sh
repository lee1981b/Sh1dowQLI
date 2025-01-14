#!/bin/bash

clear

echo -e "\e[1;35m╔══════════════════════════════════════════════════════════════════╗\e[0m"
echo -e "\e[1;36m"
echo " ███████╗██╗  ██╗ ██╗██████╗  ██████╗ ██╗    ██╗ ██████╗ ██╗     ██╗"
echo " ██╔════╝██║  ██║███║██╔══██╗██╔═══██╗██║    ██║██╔═══██╗██║     ██║"
echo " ███████╗███████║╚██║██║  ██║██║   ██║██║ █╗ ██║██║   ██║██║     ██║"
echo " ╚════██║██╔══██║ ██║██║  ██║██║   ██║██║███╗██║██║▄▄ ██║██║     ██║"
echo " ███████║██║  ██║ ██║██████╔╝╚██████╔╝╚███╔███╔╝╚██████╔╝███████╗██║"
echo " ╚══════╝╚═╝  ╚═╝ ╚═╝╚═════╝  ╚═════╝  ╚══╝╚══╝  ╚══▀▀═╝ ╚══════╝╚═╝"
echo -e "\e[0m"
echo -e "\e[1;35m╚══════════════════════════════════════════════════════════════════╝\e[0m"
echo -e "\e[1;32m╔══════════════════════════════════════════════════════════════════╗\e[0m"
echo -e "\e[1;32m|                        Made by hexsh1dow                         |\e[0m"
echo -e "\e[1;32m╚══════════════════════════════════════════════════════════════════╝\e[0m"

read -p "Enter the website URL or domain: " website_input

if [[ ! $website_input =~ ^https?:// ]]; then
    website_url="https://$website_input"
else
    website_url="$website_input"
fi

echo "Normalized URL being used: $website_url"

output_dir="output"
mkdir -p "$output_dir"

echo "$website_url" | katana -ps -pss waybackarchive,commoncrawl,alienvault -f qurl | uro > "$output_dir/output.txt"

katana -u "$website_url" -d 5 -f qurl | uro | anew "$output_dir/output.txt"

echo "Filtering URLs for potential SQLi endpoints..."

grep -Ei '(\?|&)(cid|p|id|item|cat|product|page|q|param|value)=' "$output_dir/output.txt" | grep -Ei 'union|select|--|#|and|or|like|into|from|drop|/*|' | sort -u > "$output_dir/sqli_output.txt"

if [[ -s "$output_dir/sqli_output.txt" ]]; then
    echo "Filtered SQLi URLs have been saved to: $output_dir/sqli_output.txt"
else
    echo "No SQLi URLs detected. Please check your filtering pattern or URLs."
fi

rm "$output_dir/output.txt"
