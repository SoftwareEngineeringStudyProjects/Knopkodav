# fix needed for some versions: on Mac needed, on Windows works without it?
import threading

import pyscreeze
import PIL

__PIL_TUPLE_VERSION = tuple(int(x) for x in PIL.__version__.split("."))
pyscreeze.PIL__version__ = __PIL_TUPLE_VERSION


import pyautogui

# im1 = pyautogui.screenshot()
# im1.save('test.png')
# print("image saved")
# #im1.show()
# print("done")


# print("trying to find target")
# loc = pyautogui.locateOnScreen('target.png', confidence=0.9) # locateCenterOnScreen
# print(loc)
# # print(loc.top)
# # print(loc.left)
# print("trying to click target")
# pyautogui.click(loc.left, loc.top)
# print("target clicked")
# print(loc)

# pyautogui.click('apple.png')


#pyautogui.click('check.png')

# def detect_clicks():
#     while True:
#         x, y = pyautogui.position()
#         if pyautogui.mouseDown():
#             print(f"mouse clicked x={x}, y-{y}")

async def save_image_async(name, image):
    import aiofiles

    async def save_file_async(name, data):
        async with aiofiles.open(name, "wb") as file:
            await file.write(data)

    print(f"saving image {name} on thread {threading.current_thread().ident}")
    from io import BytesIO

    buffer = BytesIO()
    image.save(buffer, format = "PNG")

    await save_file_async(name, buffer.getbuffer())
    print(f"saved image {name} on thread {threading.current_thread().ident}")


import pynput
import time
import asyncio
import threading

counter = 1
loop = asyncio.new_event_loop()


def run_event_loop():
    global loop

    def run_forever_on_thread():
        print(f"starting loop on thread {threading.current_thread().ident}\n")
        loop.run_forever()
        print(f"loop stopped on thread {threading.current_thread().ident}\n")

    loop_thread = threading.Thread(target=run_forever_on_thread)
    loop_thread.start()

def stop_recording():
    print("trying to stop recording")

    def stop_loop():
        print(f"stopping loop on thread {threading.current_thread().ident}\n")
        loop.stop()

    loop.call_soon_threadsafe(stop_loop)
    print("asked loop to stop")


def detect_keyboard(is_blocking = False):
    def on_press(key):
        try:
            print('alphanumeric key {0} pressed'.format(
                key.char))
        except AttributeError:
            print('special key {0} pressed'.format(
                key))

    def on_release(key):
        print('{0} released'.format(
            key))
        if key == pynput.keyboard.Key.esc:
            # Stop listener
            stop_recording()
            return False
    # non-blocking

    #blocking
    print("starting keyboard listener")
    if is_blocking:
        with pynput.keyboard.Listener(
                on_press=on_press,
                on_release=on_release) as listener:
            listener.join()
        print("keyboard listener stopped")
    else:
        listener = pynput.keyboard.Listener(
            on_press=on_press,
            on_release=on_release)
        listener.start()
        print("keyboard listener started in nonblocking mode")

def detect_clicks():


    def on_click(x, y, button, pressed):
        global counter
        global loop
        print('{0} at {1}'.format(
            'Pressed' if pressed else 'Released',
            (x, y)))
        if pressed:
            start_pc = time.perf_counter()
            start_pt = time.process_time()
            im = pyautogui.screenshot()
            screen_width, screen_height = im.size
            print(f"taking screenshot, perf_counter = {time.perf_counter()-start_pc}s, process_time = {time.process_time() - start_pt}s")

            print(threading.current_thread().ident)
            start_pc = time.perf_counter()
            start_pt = time.process_time()
            #im.save(f"recorded-{counter}.png")
            #loop.create_task( save_image_async(f"recorded-{counter}.png", im) )
            asyncio.run_coroutine_threadsafe(save_image_async(f"recorded-{counter}.png", im), loop)
            print(f"saving screenshot, perf_counter = {time.perf_counter() - start_pc}s, process_time = {time.process_time() - start_pt}s")
            box = get_part_box(x, y, screen_width, screen_height)
            part = im.crop(box)
            part.save(f"part-{counter}.png")
            counter += 1
        # if not pressed:
        #     # Stop listener
        #     return False

    def get_part_box(x, y, screen_width, screen_height):
        return (max(x-20, 0), max(y - 20,0), min(x + 20, screen_width), min(y + 20, screen_height))

    print("starting event loop")

    #asyncio.set_event_loop(loop)
    run_event_loop()

    print("starting mouse listener")
    listener = pynput.mouse.Listener(
        on_click=on_click
        )
    listener.start()
    detect_keyboard(is_blocking=True)
    listener.stop()
    print("stopped mouse listener")


    # while True:
    #     pass


def replay(num_parts=5):
    import time
    for i in range(num_parts):
        click_part(i)


def click_part(i, confidence_level=0.9):
    loc = pyautogui.locateOnScreen(f"part-{i + 1}.png", confidence=confidence_level)
    if loc:
        pyautogui.click(loc.left + 20, loc.top + 20)
        print(f"clicked {loc.left}, {loc.top}")
        time.sleep(3)
    else:
        print(f"not found, i={i}")

def draw_box_on_image(image, box):
    draw = PIL.ImageDraw.Draw(image)
    rectangle_shape = box #box_to_rectangle(box)
    draw.rectangle(rectangle_shape, outline="red")


def box_to_rectangle(box):
    return [box.left, box.top, box.left + box.width, box.top + box.height]


LEFT=0
TOP=1
RIGHT=2
BOTTOM=3

def is_intersection(rectangle1, rectangle2):

    if rectangle1[LEFT] > rectangle2[RIGHT] or rectangle2[LEFT] > rectangle1[RIGHT]:
        return False
    if rectangle1[TOP] > rectangle2[BOTTOM] or rectangle2[TOP] > rectangle1[BOTTOM]:
        return False
    return True

def get_max_rectangle(rectangle1, rectangle2):
    return [ min(rectangle1[LEFT], rectangle2[LEFT]),
             min(rectangle1[TOP], rectangle2[TOP]),
             max(rectangle1[RIGHT], rectangle2[RIGHT]),
             max(rectangle1[BOTTOM], rectangle2[BOTTOM]),]

def draw_all_boxes(image_path, part_path, confidence_level = 0.9):
    print(f"drawing boxes on {image_path}")
    with PIL.Image.open(image_path) as im:
        locations = pyautogui.locateAll(part_path, image_path, grayscale=True , confidence=confidence_level)
        boxes = []
        for loc in locations:
            print(f"{loc} = ({loc.left}, {loc.top}, {loc.left + loc.width}, {loc.top + loc.height}")
            rectangle = box_to_rectangle(loc)
            for index, box in enumerate(boxes):
                if is_intersection(box, rectangle):
                    boxes[index] = get_max_rectangle(box, rectangle)
                    break
            else:
                boxes.append(rectangle)

        for box in boxes:
            draw_box_on_image(im, box)
        im.save(image_path+"_boxes.png")
        print("image with boxes saved")


def locate_draw_boxes_opencv(image_path, part_path,
                             single_best_result=False, confidence_level=0.9, expected_results=0, match_gap=0):
    import cv2 as cv
    import numpy as np

    img_rgb = cv.imread(image_path)
    assert img_rgb is not None, "file could not be read, check with os.path.exists()"
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    template = cv.imread(part_path, cv.IMREAD_GRAYSCALE)
    assert template is not None, "file could not be read, check with os.path.exists()"
    w, h = template.shape[::-1]
    method = cv.TM_SQDIFF # ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR', 'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']
    res = cv.matchTemplate(img_gray, template, method)
    if single_best_result:
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
        print(f"min_val={min_val} at {min_loc}, max_val={max_val} at {max_loc}")
        if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv.rectangle(img_rgb, top_left, bottom_right, (0, 0, 255), 2)
    elif expected_results > 0 or match_gap > 0:
        flat = res.flatten()
        #indices_flat = np.argpartition(flat,expected_results)[:expected_results]
        indices_flat = np.argsort(flat) # all results, not just limited number [:expected_results]
        indices_tuple = np.unravel_index(indices_flat, res.shape)
        prev_value = 1
        found_rectangles = []
        for i, y in enumerate(indices_tuple[0]):
            x = indices_tuple[1][i]
            value = flat[indices_flat[i]]
            print(f'{i}. found at position x={x}, y={y} value={value}, increased {value / prev_value}')
            if match_gap > 0 and i > 0 and value / prev_value >= match_gap:
                print(f'larger than gap {match_gap}, stopping search')
                break
            prev_value = value

            rectangle = [x, y, x+w, y+h]
            for index, found_rect in enumerate(found_rectangles):
                if is_intersection(found_rect, rectangle):
                    #found_rectangles[index] = get_max_rectangle(found_rect, rectangle) # don't increase size
                    print(f'  similar rectangle found at index {index}, with x={found_rect[LEFT]}, y={found_rect[TOP]}')
                    break
            else:
                print(f'  similar rectangle not found, adding at index {len(found_rectangles)}')
                found_rectangles.append(rectangle)

            cv.rectangle(img_rgb, (x,y), (x + w, y + h), (0, 0, 255), 2)
            if expected_results > 0 and len(found_rectangles) >= expected_results:
                print(f'{expected_results} found, stopping search')
                break


    else:
        if method == cv.TM_SQDIFF_NORMED: # smaller values = better match
            threshold = 1 - confidence_level
            loc = np.where(res <= threshold)
        else:
            threshold = confidence_level
            loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):
            cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
    cv.imwrite(image_path+"_boxes_cv2.png", img_rgb)


def crop_image(input_path, output_path, left, top, right, bottom):
    with PIL.Image.open(input_path) as im:
        width, height = im.size
        box = (left, top, width - right, height - bottom)
        cropped = im.crop(box)
        cropped.save(output_path)


print("started detecting")
#detect_clicks()
#exit(0)
time.sleep(1)
print("starting replay...")
#replay(3)

#click_part(2, 0.8)
# locations = pyautogui.locateAll("part-1.png", "recorded-1.png", confidence=0.7)
# for loc in locations:
#     print(f"{loc} = ({loc.left}, {loc.top}, {loc.left+loc.width}, {loc.top+loc.height}")

#draw_all_boxes("recorded-1.png", "part-1.png", confidence_level=0.75)
#locate_draw_boxes_opencv("recorded-1.png", "part-1.png", confidence_level=0.93)
#crop_image("part-1.png","part-1c.png", 5, 5, 5, 5)
#draw_all_boxes("recorded-3.png", "part-3.png",confidence_level=0.9)
#locate_draw_boxes_opencv("recorded-3.png", "part-3.png", single_best_result=False, confidence_level=0.9)
#locate_draw_boxes_opencv("recorded-3.png", "part-3.png", single_best_result=False, expected_results=20)
locate_draw_boxes_opencv("recorded-1.png", "part-1.png", match_gap=10)