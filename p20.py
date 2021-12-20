import pdb
import copy

FNAME = "in20.txt"

chunks = [chunk.splitlines() for chunk in open(FNAME).read().split('\n\n')]
image_enhancement_algorithm = chunks[0][0]
assert len(image_enhancement_algorithm) == 512
base_img = [list(row.strip()) for row in chunks[1]]

# convert a 3x3 chunk into the appropriate value
def enhance_chunk(window): # window should already be serialized nine characters
    binary = window.replace('.', '0').replace('#', '1')
    val = int(binary, 2)
    return image_enhancement_algorithm[val]
#assert enhance_chunk('.' * 9) == '.' # otherwise chaos in the outer reaches
# turns out this isn't true for our input, which means we'll alternate from complete 
# '.' in the infinite border to '#', back and forth every two rounds, at least for our input

# enhance the whole image
# prefillchar is the character used to border the image on initial expansion - 
# it's whatever character currently exists in infinite border space
def enhance_image(img, prefillchar = '.'):
    
    # start by wraping with two layers of border pixels to account for the infinite nature
    # a 3x3 window would just barely overlap if we add two layers
    height = len(img)
    width = len(img[0])
    header_row = [prefillchar for _ in range(width + 4)]
    bordered_img = [header_row]
    bordered_img.append(header_row[:])
    for row in img:
        bordered_img.append([prefillchar, prefillchar] + row + [prefillchar, prefillchar])
    bordered_img.append(header_row[:])
    bordered_img.append(header_row[:])
    
    # now loop through and recalculate each pixel
    height = len(bordered_img)
    width = len(bordered_img[0])
    next_img = copy.deepcopy(bordered_img) # make a template of the same size; it's ok that it has junk in it
    for r in range(1, height - 1):
        for c in range(1, width - 1):
            top = bordered_img[r - 1][c - 1:c + 2]
            middle = bordered_img[r][c - 1:c + 2]
            bottom = bordered_img[r + 1][c - 1:c + 2]
            new_pixel = enhance_chunk(''.join(top + middle + bottom))
            next_img[r][c] = new_pixel
            
    # finalize the border
    postfillchar = enhance_chunk(prefillchar * 9) # what will happen in the outer reaches?
    for r in range(height):
        next_img[r][0] = postfillchar
        next_img[r][-1] = postfillchar
    for c in range(width):
        next_img[0][c] = postfillchar
        next_img[-1][c] = postfillchar
            
    return next_img
      
# show the img on the screen for debug purposes
def render(img):
    for row in img:
        print(''.join(row))
    print()

# count the number of instances of val in img
def count(img, val):
    return sum(row.count(val) for row in img)

# for Part 1, just two rounds
img = enhance_image(base_img, '.')
nextfill = enhance_chunk('.' * 9)
img = enhance_image(img, nextfill)
print("Part 1:", count(img, '#'))

# for Part 2, 48 more rounds (50 total)
for _ in range(48):
    nextfill = enhance_chunk(nextfill * 9)
    img = enhance_image(img, nextfill)
    
print("Part 2:", count(img, '#'))

#pdb.set_trace()
