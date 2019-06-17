# Dedup links collected
cp data/links.txt data/links.txt.bak
sort -u data/links.txt > /tmp/sorted_links.txt
mv /tmp/sorted_links.txt data/links.txt

# Dedup links done
cp data/links_done.txt data/links_done.txt.bak
sort -u data/links_done.txt > /tmp/sorted_links_done.txt
mv /tmp/sorted_links_done.txt data/links_done.txt

# links = links - links done
comm -23 data/links.txt data/links_done.txt > /tmp/pending.txt
mv /tmp/pending.txt data/links.txt
# gshuf -o data/links.txt < data/links.txt

# Dedup video links collected
cp data/video_page_links.txt data/video_page_links.txt.bak
sort -u data/video_page_links.txt > /tmp/sorted_video_page_links.txt
mv /tmp/sorted_video_page_links.txt data/video_page_links.txt

# Dedup video links done
cp data/video_page_links_done.txt data/video_page_links_done.txt.bak
sort -u data/video_page_links_done.txt > /tmp/sorted_video_page_links_done.txt
mv /tmp/sorted_video_page_links_done.txt data/video_page_links_done.txt

# video links = video links - links done
comm -23 data/video_page_links.txt data/video_page_links_done.txt > /tmp/pending2.txt
mv /tmp/pending2.txt data/video_page_links.txt

# Dedup invalid links
cp data/invalid_links.txt data/invalid_links.txt.bak
sort -u data/invalid_links.txt > /tmp/sorted_invalid_links.txt
mv /tmp/sorted_invalid_links.txt data/invalid_links.txt
