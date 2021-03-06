#!/usr/bin/env python2


def get_channels(frequency=220.352e6):
    from gnuradio import gr, blocks, audio

    import osmosdr
    import grdab

    samp_rate = samp_rate = 2000000

    print("Setting frequency: %0.3f MHz" % (frequency/1e6))

    osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + '' )
    osmosdr_source_0.set_sample_rate(samp_rate)
    osmosdr_source_0.set_center_freq(frequency, 0)
    osmosdr_source_0.set_freq_corr(80, 0)
    osmosdr_source_0.set_dc_offset_mode(0, 0)
    osmosdr_source_0.set_iq_balance_mode(0, 0)
    osmosdr_source_0.set_gain_mode(False, 0)
    osmosdr_source_0.set_gain(49, 0)
    osmosdr_source_0.set_if_gain(20, 0)
    osmosdr_source_0.set_bb_gain(20, 0)
    osmosdr_source_0.set_antenna('', 0)
    osmosdr_source_0.set_bandwidth(0, 0)

    dab_ofdm_demod_0 = grdab.ofdm_demod(
              grdab.parameters.dab_parameters(
                mode=1,
                sample_rate=samp_rate,
                verbose=False
              ),
              grdab.parameters.receiver_parameters(
                mode=1,
                softbits=True,
                input_fft_filter=True,
                autocorrect_sample_rate=False,
                sample_rate_correction_factor=1,
                verbose=False,
                correct_ffe=True,
                equalize_magnitude=True
              )
            )

    dab_fic_decode_0 = grdab.fic_decode(
              grdab.parameters.dab_parameters(
                mode=1,
                sample_rate=samp_rate,
                verbose=False
              )
            )
    dab_fic_decode_0.set_print_channel_info(True)  

    fg = gr.top_block()

    fg.connect(osmosdr_source_0, dab_ofdm_demod_0, dab_fic_decode_0)



    fg.start()
    raw_input("Running..")
    fg.stop()
