def optimal_page_replacement(pages, capacity):
    # Initialize variables to store page faults and details
    page_faults = 0
    page_frames = []
    page_fault_details = []

    # Iterate through each page reference
    for page_index, page in enumerate(pages):
        # If page is not in page frames (page fault)
        if page not in page_frames:
            # If there is space in page frames, add page
            if len(page_frames) < capacity:
                page_frames.append(page)
            else:
                # Find future occurrences of pages in page frames
                future_occurrences = {}
                for frame_index, frame in enumerate(page_frames):
                    try:
                        future_occurrences[frame] = pages.index(
                            frame, page_index)
                    except ValueError:
                        # If page is not found in the future, assign infinity
                        future_occurrences[frame] = float('inf')

                # Find the page with the farthest future occurrence
                page_to_replace = max(future_occurrences,
                                      key=future_occurrences.get)
                replaced_page = page_frames[page_frames.index(page_to_replace)]
                # Replace page in page frames
                page_frames[page_frames.index(page_to_replace)] = page

                # Record page fault details
                page_fault_details.append({
                    'page': page,
                    'replaced_page': replaced_page,
                    'page_frames': page_frames.copy(),
                    'future_occurrences': future_occurrences
                })

            page_faults += 1

    return page_faults, page_fault_details
