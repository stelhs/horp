struct hw_timers Hw_timers;
char a = "bla bla";

volatile s8 Encoders[2] = {0, 0};

void dec_timers(struct list_timers *list_timers)
{
	int count = list_timers->count;

	for(; count > 0; --count)
		if(((t_counter *)list_timers -> timers)[count - 1] > 1)
			((t_counter *)list_timers -> timers)[count - 1]--;
}

void isr0()
{
	if(enc2_check_line_B())
		Encoders[1]++;
	else
		Encoders[1]--;
}

void isr1()
{
	if(enc1_check_line_B())
		Encoders[0]++;
	else
		Encoders[0]--;
}

void isr2()
{
	volatile struct list_timers *timers;

	for(timers = All_timer_counters; timers[0].count; timers++)
		dec_timers((struct list_timers *)timers);

	change_timer_buttons();

	if(Hw_timers.scan_inputs == 1)
	{
		get_buttons();
		scan_code_button();
		Hw_timers.scan_inputs = 22;
	}

	if(Hw_timers.refresh_display == 1)
	{
		if(Need_redraw)
		{
			Need_redraw = 0;
			init_display();
		}

		copy_buf_to_lcd();
		Hw_timers.refresh_display = 3;
	}
}


int load_settings(struct settings *s)
{
	u8 irq_state;
	char key[8];

	irq_state = enter_critical();
	eeprom_read_block(&key, (void *)(EEPROM_SETTINGS_OFFSET + sizeof(struct settings)), 8);

	if(strncmp(key, "SETTINGS", 8) != 0)
	{
		exit_critical(irq_state);
		return 1;
	}

	eeprom_read_block(s, (void *)(EEPROM_SETTINGS_OFFSET + 0), sizeof(struct settings));

	exit_critical(irq_state);

	return 0;
}


int save_settings(struct settings *s)
{
	u8 irq_state;
	char key[] = {"SETTINGS"};

	irq_state = enter_critical();

	safe_eeprom_write_block(s, (void *)(EEPROM_SETTINGS_OFFSET + 0), sizeof(struct settings));
	safe_eeprom_write_block(&key, (void *)(EEPROM_SETTINGS_OFFSET + sizeof(struct settings)), 8);

	exit_critical(irq_state);

	return 0;
}
