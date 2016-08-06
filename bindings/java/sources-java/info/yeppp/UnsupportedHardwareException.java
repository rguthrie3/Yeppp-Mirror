/*
 *                      Yeppp! library implementation
 *
 * This file is part of Yeppp! library and licensed under the New BSD license.
 * See LICENSE.txt for the full text of the license.
 */

package info.yeppp;

/**
 * Unsupported hardware exception
 * <p>
 * This exception is thrown when system lacks hardware required for the requested Yeppp! function call.
 */
public class UnsupportedHardwareException extends RuntimeException {
	
	/**
	 * Constructs an unsupported hardware exception with the specified description.
	 */
	public UnsupportedHardwareException(String description) {
		super(description);
	}

}
