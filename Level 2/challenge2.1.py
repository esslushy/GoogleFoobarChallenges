def solution(l):
    # Take array l split into specific versions, change version to dictionary, sort using dictionary
    versions = [] # Array of dictionaries
    for version_number in l:
        numbers = version_number.split('.')
        parts = len(numbers)
        major = int(numbers[0])
        minor = 0
        revision = 0
        if parts>1:
            minor = int(numbers[1])
        if parts>2:
            revision = int(numbers[2])
        versions.append({
            'major': major,
            'minor': minor,
            'revision': revision,
            'parts': parts
        })
    # Sort versions. Insertion sort
    sorted_versions = []
    # Each version gets inserted into the sorted array
    for version in versions:
        for i in range(len(sorted_versions) + 1):
            try:
                # Case if major is larger
                if sorted_versions[i]['major'] < version['major']:
                    continue # Keep moving up the line
                # Case if major is smaller
                elif sorted_versions[i]['major'] > version['major']:
                    sorted_versions.insert(i, version)
                    break
                # If majors are equal, check minors
                else:
                    # If minor is larger
                    if sorted_versions[i]['minor'] < version['minor']:
                        continue # Keep moving up the line
                    # Case if minor is smaller
                    elif sorted_versions[i]['minor'] > version['minor']:
                        sorted_versions.insert(i, version)
                        break
                    # If minors are equal, check revisions
                    else:
                        # If revision is larger
                        if sorted_versions[i]['revision'] < version['revision']:
                            continue # Keep moving up the line
                        # Case if revision is smaller
                        elif sorted_versions[i]['revision'] > version['revision']:
                            sorted_versions.insert(i, version)
                            break
                        # If revision are equal, check for number of parts
                        else:
                            if sorted_versions[i]['parts'] < version['parts']:
                                continue # Keep moving up the line
                            elif sorted_versions[i]['parts'] > version['parts']:
                                sorted_versions.insert(i, version)
                                break
            except IndexError:
                sorted_versions.append(version)
    # Turn sorted version into string
    string_versions = []
    for version in sorted_versions:
        if version['parts'] == 1:
            string_versions.append(str(version['major']))
        elif version['parts'] == 2:
            string_versions.append(str(version['major']) + '.' + str(version['minor']))
        elif version['parts'] == 3:
            string_versions.append(str(version['major']) + '.' + str(version['minor']) + '.' + str(version['revision']))

    return string_versions

print(solution(['3.4.5', '2.3.4', '2', '2.0', '2.0.0']))