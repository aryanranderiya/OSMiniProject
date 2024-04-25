def optimal_page_replacement(pages, capacity):
    page_faults = 0
    page_frames = []
    page_fault_details = []

    for page in pages:
        if page not in page_frames:
            if len(page_frames) < capacity:
                page_frames.append(page)
            else:
                future_occurrences = {}
                for i in range(len(page_frames)):
                    try:
                        future_occurrences[page_frames[i]] = pages.index(
                            page_frames[i], pages.index(page))
                    except ValueError:
                        future_occurrences[page_frames[i]] = float('inf')

                page_to_replace = max(future_occurrences,
                                      key=future_occurrences.get)
                replaced_page = page_frames[page_frames.index(page_to_replace)]
                page_frames[page_frames.index(page_to_replace)] = page
                page_fault_details.append(
                    {'page': page, 'replaced_page': replaced_page, 'page_frames': page_frames.copy()})
            page_faults += 1

    return page_faults, page_fault_details
