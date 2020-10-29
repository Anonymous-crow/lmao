#from future import unicode_literals
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import base64, json, youtube_dl, pafy, threading, pygame, eyed3, pygame.midi, pygame
import twitchio as tio
import asyncio

def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()
def message_display(screen, text, x, y, size, color):
    import pygame as pg
    largeText = pg.font.Font(None, size)
    TextSurf, TextRect = text_objects(text, largeText, color)
    TextRect.center = (int(x), int(y))
    screen.blit(TextSurf, TextRect)
    dimension = largeText.render(text, True, color).get_rect()
    return [x, y, dimension[2], dimension[3]]

def miditest():
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
    import pygame, time, random, pygame.midi
    pygame.init()
    pygame.midi.init()
    i=0
    while i < pygame.midi.get_count():
        print(i, pygame.midi.get_device_info(i)); i+=1
    default_port = pygame.midi.get_default_output_id()
    print ("default device id: %s" % default_port)
    port = input('select device id[%s]: '% default_port)
    if port=='': port=default_port
    print ("using device id: %s" % port)
    midi_out = pygame.midi.Output(int(port), 0)
    pygame.init(); pygame.display.set_caption('zyntest');
    screen = pygame.display.set_mode((640, 240), pygame.RESIZABLE);
    lmao = True
    while lmao:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: lmao = False; break
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE); winw, winh = (event.w, event.h)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    midi_out.note_on(74, 127, 0)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    midi_out.note_off(74)
        screen.fill((255, 255, 255))
        message_display(screen, str(pygame.midi.get_init()), winw/2, winh/2, 200, (0,0,0))
        pygame.display.update()
    del midi_out
    pygame.midi.quit()

def midiExample():
    from time import sleep
    # Things to consider when using pygame.midi:
    #
    # 1) Initialize the midi module with a to pygame.midi.init().
    # 2) Create a midi.Output instance for the desired output device port.
    # 3) Select instruments with set_instrument() method calls.
    # 4) Play notes with note_on() and note_off() method calls.
    # 5) Call pygame.midi.Quit() when finished. Though the midi module tries
    #    to ensure that midi is properly shut down, it is best to do it
    #    explicitly. A try/finally statement is the safest way to do this.
    #
    GRAND_PIANO = 0
    CHURCH_ORGAN = 19
    instrument = CHURCH_ORGAN
    #instrument = GRAND_PIANO

    pygame.init()
    pygame.midi.init()

    port = pygame.midi.get_default_output_id()
    print ("using output_id :%s:" % port)
    print(str(pygame.midi.get_count()))
    midi_out = pygame.midi.Output(3, 0)
    try:

        midi_out.note_on(72,127) # 74 is middle C, 127 is "how loud" - max is 127
        sleep(.5)
        midi_out.note_off(72,127)
        sleep(.5)

        midi_out.note_on(76,127) # E
        sleep(.5)
        midi_out.note_off(76,127)
        sleep(.5)

        midi_out.note_on(79,127) # G
        sleep(.5)
        midi_out.note_off(79,127)
        sleep(.5)

        midi_out.note_on(72,127)
        midi_out.note_on(76,127)
        midi_out.note_on(79,127)
        sleep(.5)
        midi_out.note_off(72,127)
        midi_out.note_off(76,127)
        midi_out.note_off(79,127)

    finally:
        del midi_out
        pygame.midi.quit()
def midi_2():

    import pygame.midi

    pygame.init()
    X = 400
    Y = 400
    window = pygame.display.set_mode(size=(X, Y))
    pygame.display.set_caption('MIDI Keyboard')
    pygame.midi.init()
    i=0
    while i < pygame.midi.get_count():
        print(i, pygame.midi.get_device_info(i)); i+=1
    default_port = pygame.midi.get_default_output_id()
    print ("default device id: %s" % default_port)
    port = input('select device id[%s]: '% default_port)
    if port=='': port=default_port
    print ("using device id: %s" % port)
    midiOutput = pygame.midi.Output(int(port))
    instrument = 0
    midiOutput.set_instrument(instrument)
    octave = 0
    volume = 127

    white = (255, 255, 255)
    black = (0, 0, 0)
    print(pygame.font.get_fonts())
    font = pygame.font.SysFont('arial', 20)
    text = font.render('Q and W to change instrument: ' + str(instrument) + '', True, black, white)
    text1 = font.render('Z and X to change octave', True, black, white)
    text2 = font.render('C and V to alter the volume: ' + str(volume * 100 / 127) + '', True, black, white)
    textRect = text.get_rect()
    textRect1 = text1.get_rect()
    textRect2 = text2.get_rect()
    textRect.center = (X // 2, Y // 4)
    textRect1.center = (X // 2, Y * 2 // 4)
    textRect2.center = (X // 2, Y * 3 // 4)


    def setting(event):
        global volume
        global octave
        global instrument
        global midiOutput

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_z and octave < 7:
                octave += 1
                midiOutput.close()
                midiOutput = pygame.midi.Output(pygame.midi.get_default_output_id())
                midiOutput.set_instrument(instrument)
            if event.key == pygame.K_x and octave > -7:
                octave -= 1
                midiOutput.close()
                midiOutput = pygame.midi.Output(pygame.midi.get_default_output_id())
                midiOutput.set_instrument(instrument)
            if event.key == pygame.K_v and volume < 127:
                volume += 10
            if event.key == pygame.K_c and volume > 0:
                volume -= 10
            if event.key == pygame.K_q and instrument > 0:
                instrument -= 1
                midiOutput.close()
                midiOutput = pygame.midi.Output(0)
                midiOutput.set_instrument(instrument)
            if event.key == pygame.K_w and instrument < 127:
                instrument += 1
                midiOutput.close()
                midiOutput = pygame.midi.Output(pygame.midi.get_default_output_id())
                midiOutput.set_instrument(instrument)

        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            midiOutput.close()
            pygame.midi.quit()
            pygame.quit()
            quit()

        return


    def playSound(event):
        global volume
        global place

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                midiOutput.note_on(place - 8, volume)
            if event.key == pygame.K_s:
                midiOutput.note_on(place - 7, volume)
            if event.key == pygame.K_e:
                midiOutput.note_on(place - 6, volume)
            if event.key == pygame.K_d:
                midiOutput.note_on(place - 5, volume)
            if event.key == pygame.K_r:
                midiOutput.note_on(place - 4, volume)
            if event.key == pygame.K_f:
                midiOutput.note_on(place - 3, volume)
            if event.key == pygame.K_t:
                midiOutput.note_on(place - 2, volume)
            if event.key == pygame.K_g:
                midiOutput.note_on(place - 1, volume)
            if event.key == pygame.K_h:
                midiOutput.note_on(place, volume)
            if event.key == pygame.K_u:
                midiOutput.note_on(place + 1, volume)
            if event.key == pygame.K_j:
                midiOutput.note_on(place + 2, volume)
            if event.key == pygame.K_i:
                midiOutput.note_on(place + 3, volume)
            if event.key == pygame.K_k:
                midiOutput.note_on(place + 4, volume)
            if event.key == pygame.K_l:
                midiOutput.note_on(place + 5, volume)
            if event.key == pygame.K_p:
                midiOutput.note_on(place + 6, volume)
            if event.key == pygame.K_n:
                midiOutput.note_on(place + 7, volume)
            if event.key == pygame.K_m:
                midiOutput.note_on(place + 8, volume)

        if event.type == pygame.KEYUP:

            if event.key == pygame.K_a:
                midiOutput.note_off(place - 8, volume)
            if event.key == pygame.K_s:
                midiOutput.note_off(place - 7, volume)
            if event.key == pygame.K_e:
                midiOutput.note_off(place - 6, volume)
            if event.key == pygame.K_d:
                midiOutput.note_off(place - 5, volume)
            if event.key == pygame.K_r:
                midiOutput.note_off(place - 4, volume)
            if event.key == pygame.K_f:
                midiOutput.note_off(place - 3, volume)
            if event.key == pygame.K_t:
                midiOutput.note_off(place - 2, volume)
            if event.key == pygame.K_g:
                midiOutput.note_off(place - 1, volume)
            if event.key == pygame.K_h:
                midiOutput.note_off(place, volume)
            if event.key == pygame.K_u:
                midiOutput.note_off(place + 1, volume)
            if event.key == pygame.K_j:
                midiOutput.note_off(place + 2, volume)
            if event.key == pygame.K_i:
                midiOutput.note_off(place + 3, volume)
            if event.key == pygame.K_k:
                midiOutput.note_off(place + 4, volume)
            if event.key == pygame.K_l:
                midiOutput.note_off(place + 5, volume)
            if event.key == pygame.K_p:
                midiOutput.note_off(place + 6, volume)
            if event.key == pygame.K_n:
                midiOutput.note_off(place + 7, volume)
            if event.key == pygame.K_m:
                midiOutput.note_off(place + 8, volume)

            return


    while True:
        place = 68 - octave * 8
        text = font.render('Q and W to change instrument: ' + str(instrument) + '', True, black, white)
        text1 = font.render('Z and X to change octave: ' + str(octave) + '', True, black, white)
        text2 = font.render('C and V to alter the volume: ' + str(volume * 100 // 127) + '', True, black, white)
        window.fill(white)
        window.blit(text, textRect)
        window.blit(text1, textRect1)
        window.blit(text2, textRect2)
        pygame.display.update()
        pygame.time.wait(16)
        for event in pygame.event.get():
            setting(event)
            playSound(event)
midi_2()
