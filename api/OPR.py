def optimal_page_replacement(pages, capacity):
    """
    Performs Optimal Page Replacement algorithm.

    Parameters:
        pages (list of int): Sequence of page references.
        capacity (int): Capacity of page frames.

    Returns:
        tuple: A tuple containing:
            - int: Number of page faults that occurred during the replacement process.
            - list of dicts: Details of each page fault, including the page replaced and current state of page frames.
    """
    page_faults = 0  # Initialize page fault counter
    page_frames = []  # Initialize list to store page frames
    page_fault_details = []  # Initialize list to store details of each page fault

    for page in pages:  # Iterate through each page reference
        # If page is not already in page frames (page fault)
        if page not in page_frames:
            if len(page_frames) < capacity:  # If there is space in page frames
                page_frames.append(page)  # Add page to page frames
            else:
                # Initialize dictionary to store future occurrences of pages in page frames
                future_occurrences = {}
                for i in range(len(page_frames)):  # Iterate through each page frame
                    try:
                        # Find index of next occurrence of the page in the sequence after the current page
                        future_occurrences[page_frames[i]] = pages.index(
                            page_frames[i], pages.index(page))
                    except ValueError:
                        # If page is not found in the sequence after the current page, assign infinity
                        future_occurrences[page_frames[i]] = float('inf')

                # Find the page in page frames with the farthest future occurrence
                page_to_replace = max(future_occurrences,
                                      key=future_occurrences.get)
                replaced_page = page_frames[page_frames.index(
                    page_to_replace)]  # Get page to be replaced
                page_frames[page_frames.index(
                    page_to_replace)] = page  # Replace page
                # Append details of page fault to page_fault_details list
                page_fault_details.append({'page': page, 'replaced_page': replaced_page,
                                           'page_frames': page_frames.copy()})
            page_faults += 1  # Increment page fault counter

    # Return number of page faults and page fault details
    return page_faults, page_fault_details
